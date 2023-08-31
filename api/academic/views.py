from rest_framework import views, viewsets
from rest_framework.decorators import action
from api.academic.serializers import *
from api.academic.models import *
from api.forums.models import Forum, TopicMessageReadBy
from api.forums.serializers import *
from api.monitoring.models import ClassJournal
from api.users.models import User
from api.permissions import CustomPermission
from rest_framework.response import Response
from rest_framework import status
from api.institutions.models import InstitutionLevel

import pandas as pd

# Create your views here.


class ProgramViewSet(viewsets.ModelViewSet):
    serializer_class = ProgramSerializer
    queryset = Program.objects.all()
    permission_classes = [CustomPermission]

    def create(self, request):
        try:
            data = request.data
            lessons = []
            if 'lessons' in data:
                lessons = data['lessons']
                del data['lessons']

            lic = None
            if 'licenss' in data:
                lic = License.objects.get(pk=int(data['licenss']))
                del data['licenss']

            p = Program(**data, licenss=lic)
            p.save()
            for lesson in lessons:
                lp = LessonProgram(lesson=Lesson.objects.get(pk=int(lesson['id'])), program=p, lesson_number=int(
                    lesson['lesson_number']), term=int(lesson['term']))
                lp.save()

            for term in LessonProgram.TERM_OPTIONS:
                lps = sorted(list(p.lesson_program.filter(
                    term=term[0])), key=lambda x: x.lesson_number)
                if lps:
                    for i in range(0, len(lps)-1):
                        lps[i].next_lesson = lps[i+1]
                        lps[i].save()

            return Response({'message': f'program {p.name} created', 'id': p.id}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'])
    def lessons(self, request, pk=None):
        try:
            program = Program.objects.get(pk=pk)
            lps = sorted(LessonProgram.objects.filter(
                program=program), key=lambda x: x.lesson_number)
            program.n_lessons = len(lps)
            program.save()
            data = LessonProgramSerializer(lps, many=True).data
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def upload(self, request):
        try:
            uploaded_file = request.FILES.get("file")
            errors = {}
            if uploaded_file is not None:
                reader = pd.read_csv(uploaded_file)
                i = 0
                for _, row in reader.iterrows():
                    try:
                        qs = License.objects.filter(name=row['licenss'])
                        if not qs.exists():
                            lic = License(name=row['licenss'])
                            lic.save()
                        else:
                            lic = License.objects.get(name=row['licenss'])
                        del row['licenss']

                        row = {key: value for key,
                               value in row.items() if pd.notna(value)}

                        program = Program(**row, licenss=lic)
                        program.save()
                    except Exception as e:
                        errors[f'Row {i}:'] = str(e)

                    i = i+1

                if errors == {}:
                    return Response({'status': 'Programas creados'}, status=status.HTTP_201_CREATED)
                else:
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'error': 'file error'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [CustomPermission]

    def list(self, request):
        try:
            allowed_roles = ['academic_coordination', 'academy_coordination',
                             'directors', 'IT', 'monitoring_coordinator']
            qs = []
            user = request.user

            if not request.user.role in allowed_roles:
                if user.teacher_profile and user.role == 'external_teacher' or user.role == 'internal_teacher':
                    qs = Course.objects.filter(teachers=user.teacher_profile)
                else:
                    levels = InstitutionLevel.objects.all()
                    if user.role == 'monitoring_teacher':
                        levels = levels.filter(institution__monitor=user)
                    elif user.role == 'external_coordinator':
                        levels = levels.filter(institution_coordinator=user)

                    for level in levels:
                        for c in level.courses.all():
                            qs.append(c)

            else:
                qs = self.queryset

            data = []

            context = {
                'excluded_fields': [
                    'organization',
                    'date_joined',
                    'address',
                    'city',
                    'state',
                    'monitor',
                    'classrooms_per_level',
                    'students_per_classroom',
                    'ocupancy_rate',
                    'teacher_service',
                    'lessons',
                    'teachers',
                ]
            }

            for c in qs:
                d = CourseSerializer(c, context=context).data
                d['unread_forum'] = False

                topics = c.forum.forum_topics.all()
                for topic in topics:
                    if topic.getNumberOfMessages() > len(TopicMessageReadBy.objects.filter(user=request.user, message__topic=topic)):
                        d['unread_forum'] = True
                        break

                data.append(d)

            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)})

    def retrieve(self, request, pk=None):

        context = {'excluded_fields': ['class_journal',]}

        try:
            user = request.user
            course = Course.objects.get(pk=pk)
            role = user.role

            teacher_is_allowed = user.teacher_profile and course.teachers.filter(
                id=user.teacher_profile.id).exists()

            allowed_roles = ['academic_coordination', 'academy_coordination',
                             'directors', 'IT', 'monitoring_coordinator']

            if ((user.teacher_profile and role.endswith('_teacher') and teacher_is_allowed) or
                (user.role == 'external_coordinator' and course.institution_level.institution_coordinator.id == user.id) or
                (user.role == 'monitoring_teacher' and course.institution_level.institution.monitor.id == user.id) or
                (user.role in allowed_roles) or
                    user.is_superuser):

                context = {
                    'excluded_fields': [
                        'organization',
                        'date_joined',
                        'address',
                        'city',
                        'state',
                        'classrooms_per_level',
                        'students_per_classroom',
                        'ocupancy_rate',
                        'distributor',
                        'course_outline',
                        'planification_term1',
                        'planification_term2',
                        'planification_term3',
                        'employees',
                        'lessons',
                        'stages',
                        'teachers',
                    ]
                }

                data = CourseSerializer(course, context=context).data
                data['unread_forum'] = False

                topics = course.forum.forum_topics.all()
                for topic in topics:
                    if topic.getNumberOfMessages() > len(TopicMessageReadBy.objects.filter(user=request.user, message__topic=topic)):
                        data['unread_forum'] = True
                        break

                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        try:
            program = request.data['program']
            levels = request.data['levels']
            start_date = request.data['start_date']
            end_date = request.data['end_date']
            is_curricular = request.data['is_curricular']

            if (is_curricular):
                year = AcademicYear.objects.get(pk=int(request.data['year']))
                for level in levels:
                    new_course = Course(
                        program=Program.objects.get(pk=program),
                        institution_level=InstitutionLevel.objects.get(
                            pk=int(level)),
                        year=year,
                        start_date=start_date if start_date != None else year.start_date,
                        end_date=end_date if end_date != None else year.end_date
                    )

                    new_course.save()
                    forum = Forum(description='', course=new_course)
                    forum.save()
            else:
                for level in levels:
                    new_course = Course(
                        program=Program.objects.get(pk=program),
                        institution_level=InstitutionLevel.objects.get(
                            pk=int(level)),
                        start_date=start_date if start_date != None else year.start_date,
                        end_date=end_date if end_date != None else year.end_date
                    )

                    new_course.save()
                    forum = Forum(description='', course=new_course)
                    forum.save()

            return Response({'message': f"Forum: {forum.id} / Course: {new_course.id}"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def sections(self, request, pk=None):
        try:
            course = Course.objects.get(pk=pk)
            sections = CourseSectionSerializer(course.sections, many=True)
            return Response(sections.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def forum(self, request, pk=None):
        try:
            course = Course.objects.get(pk=pk)
            forum = Forum.objects.get(course=course)

            context = {
                'excluded_fields': [
                    'forum',
                    'lesson',
                ]
            }

            data = ForumSerializer(forum, context=context).data
            data['topics'] = []

            topics = forum.forum_topics.all()
            for topic in topics:
                d = ForumTopicSerializer(topic).data
                d['unread_messages'] = False
                if topic.getNumberOfMessages() > len(TopicMessageReadBy.objects.filter(user=request.user, message__topic=topic)):
                    d['unread_messages'] = True

                data['topics'].append(d)

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def lessons(self, request, pk=None):
        try:
            course = Course.objects.get(pk=pk)
            lessons = course.program.getLessons()

            for term in lessons:
                lessons[term] = LessonSerializer(lessons[term], many=True).data
                for lesson in lessons[term]:
                    for section in course.sections.all():
                        l=Lesson.objects.get(pk=lesson['id'])
                        qs = ClassJournal.objects.filter(
                            lesson=l, section=section)
                        if qs.exists():
                            cj = qs
                            lesson['class_journal'] = ClassJournalSerializer(
                                cj, many=True).data
                        else:
                            lesson['class_journal'] = {}

            return Response(lessons, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['PATCH'])
    def register(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
            course.teachers.add(request.user.teacher_profile)
            course.save()

            forum = course.forum
            forum.members.add(request.user)
            forum.save()

            return Response({'message': 'teacher registered in course', 'course': CourseSerializer(course).data}, status=status.HTTP_200_OK)

        except Exception as e:
            raise e
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def upload(self, request):
        try:
            uploaded_file = request.FILES.get("file")
            errors = {}
            if uploaded_file is not None:
                reader = pd.read_csv(uploaded_file)
                i = 0
                for _, row in reader.iterrows():
                    try:
                        institution = Institution.objects.get(
                            name=row["institution"])
                        institution_level = InstitutionLevel.objects.get(
                            name=row["grade"], institution=institution.id)
                        program = Program.objects.get(name=row["program"])
                        year = AcademicYear.objects.get(name=row["year"])
                        del row['institution']
                        del row['grade']
                        del row['program']
                        del row['year']
                        course = Course(
                            **row, institution_level=institution_level, program=program, year=year)
                        course.save()
                        forum = Forum(description='', course=course)
                        forum.members.add(institution.monitor)
                        forum.save()
                    except Exception as e:
                        errors[f'Row {i}:'] = str(e)

                    i = i+1

                if errors == {}:
                    return Response({'status': 'Cursos creados'}, status=status.HTTP_201_CREATED)
                else:
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'error': 'file error'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ResourceViewSet(viewsets.ModelViewSet):
    serializer_class = ResourceSerializer
    queryset = Resource.objects.all()
    permission_classes = [CustomPermission]


class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [CustomPermission]

    @action(detail=False, methods=['POST'])
    def upload(self, request):
        try:
            uploaded_file = request.FILES.get("file")
            program = Program.objects.get(pk=int(request.data['program']))
            stage = request.data['stage']
            lps = []

            if uploaded_file is not None:

                # Preescolar
                if stage == "Preescolar":
                    lesson_number = 1
                    sheets = pd.read_excel(
                        uploaded_file, sheet_name=None).keys()
                    for k in sheets:
                        file = pd.read_excel(uploaded_file, sheet_name=k)
                        rows = [r for r in pd.DataFrame(file).iterrows()]
                        name = rows[1][1][5].strip().replace(
                            '.', '').capitalize()
                        term = rows[1][1][8].strip().upper()

                        if term == "I":
                            term = 1
                        elif term == "II":
                            term = 2
                        elif term == "III":
                            term = 3

                        file = pd.read_excel(
                            uploaded_file, skiprows=5, sheet_name=k)
                        columns = [i for i in file.keys()[1:]]
                        df = pd.DataFrame(file, columns=columns)
                        rows = [r[1] for r in df.iterrows()]
                        i = 0
                        lesson = Lesson(
                            title=name, licens=program.licenss, stage=stage)
                        indicator = AchievementIndicator()
                        for r in rows:
                            if all(type(p) == type(float()) for p in r):
                                break

                            learning_subject = None
                            learning_topic = None
                            goal = None
                            learning_outcome = None

                            if i == 0:
                                lesson.beginning = r[4]
                                lesson.development = r[5]
                                lesson.closure = r[6]
                                lesson.achievement_indicators = r[7]
                                lesson.save()
                                # indicator.lesson = lesson
                                # indicator.save()

                            # AL CARGAR EL CURRICULUM DEBO VERIFICAR QUE NO SE CREEN DUPLICADOS CON EL MISMO CONTENIDO
                            # EN CADA UNO DE LOS CAMPOS

                            if type(r[0]) != type(float()) and r[0] != 'nan':

                                subject = r[0].strip().replace('.', '')

                                # Verificar si un learning subject con el m ismo content existe, si no crearlo
                                # Esta apuntando al lesson, el que deberia apuntar al lesson es el Learning Outcome
                                if LearningSubject.objects.filter(content=subject).exists():
                                    learning_subject = LearningSubject.objects.get(
                                        content=subject)
                                else:
                                    learning_subject = LearningSubject(
                                        content=subject)
                                    learning_subject.save()

                            if type(r[1]) != type(float()) and r[1] != 'nan':

                                topic = r[1].strip().replace('.', '')

                                # Evaluar si el learning outcome existe, y tiene como subject el de la fila,
                                # solo crearlo si no existe

                                if LearningTopic.objects.filter(content=topic).exists():
                                    learning_topic = LearningTopic.objects.get(
                                        content=topic)
                                else:
                                    learning_topic = LearningTopic(
                                        content=topic, learning_subject=learning_subject)
                                    learning_topic.save()

                            if type(r[2]) != type(float()) and r[2] != 'nan':

                                goal = r[2].strip().replace('.', '')

                                # Evaluar si el learning outcome existe, donde el topic y el subject sea el de la fila,
                                # solo crearlo si no existe

                                if PreschoolGoal.objects.filter(content=goal).exists():
                                    goal = PreschoolGoal.objects.get(
                                        content=goal)
                                else:
                                    goal = PreschoolGoal(
                                        content=goal, component=learning_topic)
                                    goal.save()

                            if type(r[3]) != type(float()) and r[3] != 'nan':

                                outcome = r[3].strip().replace(
                                    '.', '').capitalize()

                                # Evaluar si el learning outcome existe, con el goal, topic y subject de la fila
                                # solo crearlo si no existe y signarle a esta lesson ese goal

                                if LearningOutcome.objects.filter(content=outcome).exists():
                                    learning_outcome = LearningOutcome.objects.get(
                                        content=outcome)

                                # Una lesson puede tener multiples learning outcomes y un learning outcome puede tener multiples
                                # lessons

                                else:
                                    learning_outcome = LearningOutcome(
                                        content=outcome, goal=goal)
                                    learning_outcome.save()

                                lesson.learning_outcomes.add(learning_outcome)

                            i += 1

                        k = 1
                        optional = False
                        for r in rows[i:]:

                            if r[0] in ["Presentacion", "Presentación", "Slides"]:
                                lesson.slides = r[2]
                                lesson.save()

                            if type(r[2]) != type(float()) and r[2] != 'nan':
                                if "Recurso" in r[0] or "Resource" in r[0]:
                                    url = r[2]
                                    resource = Resource(
                                        name=f"{program.name} - {name} - Recurso: {k}", program=program, number=k, url=url, type="RESOURCE")
                                    resource.save()
                                    lesson.resources.add(resource)
                                    k += 1

                            if r[4] == "MATERIAL DE CLASE (OPCIONAL)":
                                optional = True

                            if type(r[4]) != type(float()) and r[4] != "MATERIAL DE CLASE" and r[4] != "MATERIAL DE CLASE (OPCIONAL)":
                                if ClassMaterial.objects.filter(content=r[4], optional=optional).exists():
                                    m = ClassMaterial.objects.get(
                                        content=r[4], optional=optional)

                                else:
                                    m = ClassMaterial(
                                        content=r[4], optional=optional)
                                    m.save()
                                lesson.materials.add(m)

                        lp = LessonProgram(
                            lesson=lesson, program=program, term=term, lesson_number=lesson_number)
                        lp.save()
                        lps.append(lp)
                        lesson_number += 1

                elif stage.startswith("Primaria"):
                    lesson_number = 1
                    sheets = pd.read_excel(
                        uploaded_file, sheet_name=None).keys()
                    for k in sheets:
                        file = pd.read_excel(uploaded_file, sheet_name=k)
                        rows = [r for r in pd.DataFrame(file).iterrows()]
                        name = rows[1][1][6].strip().replace(
                            ".", "").capitalize()
                        term = rows[1][1][9].strip().upper()
                        file = pd.read_excel(
                            uploaded_file, skiprows=5, sheet_name=k)

                        columns = [i for i in file.keys()[1:]]
                        df = pd.DataFrame(file, columns=columns)
                        rows = [r[1] for r in df.iterrows()]
                        i = 0
                        lesson = Lesson(
                            title=name, licens=program.licenss, stage=stage)
                        # indicator = AchievementIndicator()
                        for r in rows:
                            if all(type(i) == type(float()) for i in r):
                                break

                            learning_subject = None
                            learning_topic = None
                            goal = None
                            learning_outcome = None

                            if i == 0:
                                lesson.beginning = r[5]
                                lesson.development = r[6]
                                lesson.closure = r[7]
                                lesson.main_activities = r[8]
                                lesson.achievement_indicators = r[4]
                                lesson.lesson_goal = r[3]
                                lesson.save()
                                # indicator.content = r[4]
                                # indicator.lesson = lesson
                                # indicator.save()
                                # g = Goal(content=r[3], lesson=lesson)
                                # g.save()

                            if type(r[0]) != type(float()) and r[0] != 'nan':

                                subject = r[0].strip().replace(".", "")

                                if LearningSubject.objects.filter(content=subject).exists():
                                    learning_subject = LearningSubject.objects.get(
                                        content=subject)
                                else:
                                    learning_subject = LearningSubject(
                                        content=subject)
                                    learning_subject.save()

                            if type(r[1]) != type(float()) and r[1] != 'nan':

                                topic = r[1].strip().replace(".", "")

                                if LearningTopic.objects.filter(content=topic).exists():
                                    learning_topic = LearningTopic.objects.get(
                                        content=topic)

                                else:
                                    learning_topic = LearningTopic(
                                        content=topic, learning_subject=learning_subject)
                                    learning_topic.save()

                            if type(r[2]) != type(float()) and r[2] != 'nan':

                                content = r[2].strip().replace(
                                    ".", "").capitalize()

                                if CurricularContent.objects.filter(content=content).exists():
                                    curriculum_content = CurricularContent.objects.get(
                                        content=content)
                                else:
                                    curriculum_content = CurricularContent(
                                        content=content, component=learning_topic)
                                    curriculum_content.save()
                                lesson.curriculum_content.add(
                                    curriculum_content)

                            i += 1
                        lesson.save()

                        if term == "I":
                            term = 1
                        elif term == "II":
                            term = 2
                        elif term == "III":
                            term = 3

                        k = 1
                        j = 1
                        optional = False
                        for r in rows[i:]:
                            if r[0] in ["Presentacion", "Presentación", "Slides"]:
                                lesson.slides = r[2]
                                lesson.save()
                            elif r[0] in ["Script"]:
                                lesson.script = r[2]
                                lesson.save()

                            if type(r[2]) != type(float()) and r[2] != 'nan':
                                if "Recurso" in r[0] or "Resource" in r[0]:
                                    url = r[2]
                                    resource = Resource(
                                        name=f"{program.name} - {name} - Recurso: {k}", program=program, number=k, url=url, type="RESOURCE")
                                    resource.save()
                                    lesson.resources.add(resource)
                                    k += 1
                                elif r[0] in ["Programa", "Program", "Nivel Avanzado"]:
                                    url = r[2]
                                    resource = Resource(
                                        name=f"{program.name} - {name} - Programa: {k}", program=program, url=url, type="PROGRAM")
                                    resource.save()
                                    lesson.resources.add(resource)
                                    k += 1
                            if type(r[6]) != type(float()) and r[6] != 'nan':
                                if "Captura" in r[4] or "Screenshot" in r[4]:
                                    url = r[6]
                                    resource = Resource(
                                        name=f"{program.name} - {name} - Captura: {j}", program=program, number=j, url=url, type="SCREENSHOT")
                                    resource.save()
                                    lesson.resources.add(resource)
                                    j += 1

                        lp = LessonProgram(
                            lesson=lesson, program=program, term=term, lesson_number=lesson_number)
                        lp.save()
                        lps.append(lp)
                        lesson_number += 1

                elif stage == "Bachillerato":
                    lesson_number = 1
                    sheets = pd.read_excel(
                        uploaded_file, sheet_name=None).keys()
                    for k in sheets:
                        file = pd.read_excel(uploaded_file, sheet_name=k)
                        rows = [r for r in pd.DataFrame(file).iterrows()]
                        name = rows[1][1][6].strip().replace(
                            ".", "").capitalize()
                        term = rows[1][1][9].strip().upper()
                        file = pd.read_excel(
                            uploaded_file, skiprows=5, sheet_name=k)
                        columns = [i for i in file.keys()[1:]]
                        df = pd.DataFrame(file, columns=columns)
                        rows = [r[1] for r in df.iterrows()]
                        i = 0
                        lesson = Lesson(
                            title=name, licens=program.licenss, stage=stage)
                        # indicator = AchievementIndicator()
                        for r in rows:
                            if all(type(i) == type(float()) for i in r):
                                break

                            learning_subject = None
                            learning_topic = None
                            goal = None
                            learning_outcome = None

                            if i == 0:
                                lesson.beginning = r[5]
                                lesson.development = r[6]
                                lesson.closure = r[7]
                                lesson.main_activities = r[8] if type(
                                    r[8]) != 'nan' else ""
                                lesson.lesson_goal = r[4]
                                lesson.save()
                                # indicator.content = r[4]
                                # indicator.lesson = lesson
                                # indicator.save()

                            if type(r[0]) != type(float()) and r[0] != 'nan':

                                subject = r[0].strip().replace(".", "")

                                if LearningSubject.objects.filter(content=subject).exists():
                                    learning_subject = LearningSubject.objects.get(
                                        content=subject)
                                else:
                                    learning_subject = LearningSubject(
                                        content=subject)
                                    learning_subject.save()

                            if type(r[1]) != type(float()) and r[1] != 'nan':

                                gen_topic = r[1].strip().replace(".", "")

                                if GeneratingTopic.objects.filter(content=gen_topic).exists():
                                    generating_topic = GeneratingTopic.objects.get(
                                        content=gen_topic)
                                else:
                                    generating_topic = GeneratingTopic(
                                        content=gen_topic, learning_subject=learning_subject)
                                    generating_topic.save()

                            if type(r[2]) != type(float()) and r[2] != 'nan':

                                top = r[2].strip().replace(".", "")

                                if Topic.objects.filter(content=top).exists():
                                    topic = Topic.objects.get(content=top)
                                else:
                                    topic = Topic(
                                        content=top, generating_topic=generating_topic)
                                    topic.save()

                            if type(r[3]) != type(float()) and r[3] != 'nan':

                                reference = r[3].strip().replace(
                                    ".", "").capitalize()

                                if TPReference.objects.filter(content=reference).exists():
                                    tp_reference = TPReference.objects.get(
                                        content=reference)
                                else:
                                    tp_reference = TPReference(
                                        content=reference, topic=topic)
                                    tp_reference.save()

                                lesson.curriculum_references.add(
                                    tp_reference)
                            i += 1

                        k = 1
                        j = 1
                        optional = False
                        for r in rows[i:]:
                            if r[0] in ["Presentacion", "Presentación", "Slides"]:
                                lesson.slides = r[2]
                                lesson.save()
                            elif r[0] in ["Script"]:
                                lesson.script = r[2]
                                lesson.save()

                            if type(r[2]) != type(float()) and r[2] != 'nan':
                                if "Recurso" in r[0] or "Resource" in r[0]:
                                    url = r[2]
                                    resource = Resource(
                                        name=f"{program.name} - {name} - Recurso: {k}", program=program, number=k, url=url, type="RESOURCE")
                                    resource.save()
                                    lesson.resources.add(resource)
                                    k += 1
                                elif r[0] in ["Programa", "Program", "Nivel Avanzado"]:
                                    url = r[2]
                                    resource = Resource(
                                        name=f"{program.name} - {name} - Programa: {k}", program=program, url=url, type="PROGRAM")
                                    resource.save()
                                    lesson.resources.add(resource)
                                    k += 1
                            if type(r[6]) != type(float()) and r[6] != 'nan':
                                if "Captura" in r[4] or "Screenshot" in r[4]:
                                    url = r[6]
                                    resource = Resource(
                                        name=f"{program.name} - {name} - Captura: {j}", program=program, number=j, url=url, type="SCREENSHOT")
                                    resource.save()
                                    lesson.resources.add(resource)
                                    j += 1

                        if term == "I":
                            term = 1
                        elif term == "II":
                            term = 2
                        elif term == "III":
                            term = 3

                        lp = LessonProgram(
                            lesson=lesson, program=program, term=term, lesson_number=lesson_number)
                        lp.save()
                        lps.append(lp)
                        lesson_number += 1

            else:
                return Response({'error': "File error"}, status=status.HTTP_400_BAD_REQUEST)

            if len(lps) > 0:
                for i in range(0, len(lps)-1):
                    lps[i].next_lesson = lps[i+1]
                    lps[i].save()

            program.n_lessons += len(lps)
            program.save()
            return Response({"message": "lessons created"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LessonProgramViewSet(viewsets.ModelViewSet):
    serializer_class = LessonProgramSerializer
    queryset = LessonProgram.objects.all()
    permission_classes = [CustomPermission]


class AcademicYearViewSet(viewsets.ModelViewSet):
    serializer_class = AcademicYearSerializer
    queryset = AcademicYear.objects.all()
    permission_classes = [CustomPermission]


class CourseSectionViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSectionSerializer
    queryset = CourseSection.objects.all()
    permission_classes = [CustomPermission]

    def create(self, request):
        try:
            data = request.data
            data['course'] = Course.objects.get(pk=data['course'])
            cs = CourseSection(**data)
            cs.save()

            lps = sorted(list(cs.course.program.lesson_program.all()),
                         key=lambda x: x.lesson_number)
            if len(lps) > 0:
                cs.next_lesson = lps[0]
                cs.save()
            return Response({'message': 'created'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            raise e
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LicenseViewSet(viewsets.ModelViewSet):
    serializer_class = LicenseSerializer
    queryset = License.objects.all()
    permission_classes = [CustomPermission]


class AchievementIndicatorViewSet(viewsets.ModelViewSet):
    serializer_class = AchievementIndicatorSerializer
    queryset = AchievementIndicator.objects.all()
    permission_classes = [CustomPermission]


class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    queryset = Goal.objects.all()
    permission_classes = [CustomPermission]


class LearningOutcomeViewSet(viewsets.ModelViewSet):
    serializer_class = LearningOutcomeSerializer
    queryset = LearningOutcome.objects.all()
    permission_classes = [CustomPermission]

    def create(self, request):
        try:
            data = request.data
            data['lesson'] = Lesson.objects.get(pk=data['lesson'])
            data['objective'] = PreschoolGoal.objects.get(pk=data['objective'])
            lo = LearningOutcome(**data)
            lo.save()
            return Response({'message': 'learning outcome created'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PreschoolGoalViewSet(viewsets.ModelViewSet):
    serializer_class = PreschoolGoalSerializer
    queryset = PreschoolGoal.objects.all()
    permission_classes = [CustomPermission]


class CurricularContentViewSet(viewsets.ModelViewSet):
    serializer_class = CurricularContentSerializer
    queryset = CurricularContent.objects.all()
    permission_classes = [CustomPermission]

    def create(self, request):
        try:
            data = request.data
            data['lesson'] = Lesson.objects.get(pk=data['lesson'])
            data['component'] = LearningTopic.objects.get(pk=data['component'])
            cc = CurricularContent(**data)
            cc.save()
            return Response({'message': 'Curricular Content created'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LearningTopicViewSet(viewsets.ModelViewSet):
    serializer_class = LearningTopicSerializer
    queryset = LearningTopic.objects.all()
    permission_classes = [CustomPermission]


class TPReferenceViewSet(viewsets.ModelViewSet):
    serializer_class = TPReferenceSerializer
    queryset = TPReference.objects.all()
    permission_classes = [CustomPermission]

    def create(self, request):
        try:
            data = request.data
            data['lesson'] = Lesson.objects.get(pk=data['lesson'])
            data['topic'] = Topic.objects.get(pk=data['topic'])
            t = Topic(**data)
            t.save()
            return Response({'message': 'TPReference created'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TopicViewSet(viewsets.ModelViewSet):
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()
    permission_classes = [CustomPermission]


class GeneratingTopicViewSet(viewsets.ModelViewSet):
    serializer_class = GeneratingTopicSerializer
    queryset = GeneratingTopic.objects.all()
    permission_classes = [CustomPermission]


class LearningSubjectViewSet(viewsets.ModelViewSet):
    serializer_class = LearningSubjectSerializer
    queryset = LearningSubject.objects.all()
    permission_classes = [CustomPermission]


class ClassScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = ClassScheduleSerializer
    queryset = ClassSchedule.objects.all()
    permission_classes = [CustomPermission]

    def create(self, request):
        try:
            data = request.data
            teacher = request.user
            if 'teacher' in data.keys():
                if data['teacher'] != '':
                    teacher = User.objects.get(pk=data['teacher'])
                del data['teacher']

            course_section = CourseSection.objects.get(
                pk=data['course_section'])
            del data['course_section']

            cs = ClassSchedule(
                teacher=teacher, course_section=course_section, **data)
            cs.save()

            data = ClassScheduleSerializer(cs).data

            return Response({'message': 'class journal created', 'class_journal': data}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
