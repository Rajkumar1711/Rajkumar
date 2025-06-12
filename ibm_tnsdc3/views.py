from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from ibm_tnsdc3.models import *
from .serializers import *
from django.db.models import Q
from django.db.models import F
import jwt
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.forms.models import model_to_dict

import logging
log = logging.getLogger(__name__)


# class UserAPIView(APIView):
#     """
#     View to list users based on email id.
#     """

#     permission_classes = [IsAuthenticated]

#     def get(self, request, token=None,format=None):
#         email = request.query_params.get('email')
#         if not email:
#             return Response({'error': 'email is required'}, status=status.HTTP_400_BAD_REQUEST)      
#         try:
#             user = User.objects.get(email=email)
#             if user is not None:
#                 data = {"user_info": []}
#                 data["user_info"] = {
#                     "id":user.id,
#                     "email": user.email,
#                     "first_name": user.first_name,
#                     "last_name": user.last_name,
#                     "role":user.role,
#                     "course_id": user.course_id,
#                     "college": user.college.college_name if hasattr(user, 'college') and hasattr(user.college, 'college_name') else None
#                 }
#                 return JsonResponse(data, safe=False) 
#         except User.DoesNotExist: 
#             return JsonResponse({"error": "User not found"},status=status.HTTP_404_NOT_FOUND)
#         else:
#             return JsonResponse({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, token=None,format=None):
        email = request.query_params.get('email')
        if not email:
            return Response({'error': 'email is required'}, status=status.HTTP_400_BAD_REQUEST) 
        
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise AuthenticationFailed("Invalid or missing token")
        
        token = auth_header.split(" ")[1]
        logging.info(token)
        try:
            token_data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            logging.info(token_data)
            user_id = token_data['user_id']
            logging.info(user_id)
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")
             
        try:
            user = User.objects.get(email=email)
            if user is not None:
                data = {"user_info": []}
                data["user_info"] = {
                    "id":user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role":user.role,
                    "course_id": user.course_id,
                    "college": user.college.college_name if hasattr(user, 'college') and hasattr(user.college, 'college_name') else None
                }
                return JsonResponse(data, safe=False) 
        except User.DoesNotExist: 
            return JsonResponse({"error": "User not found"},status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class NewTeamMembersAPIView(APIView):
    """
    View to list, create and update TeamMembers based on email & team_name
    """ 
    permission_classes = [IsAuthenticated]


    def get(self, request, format=None):
        logging.info(request.data)
        email = request.query_params.get('email')
        team_name = request.query_params.get('team_name')
        if not email or not team_name:
            return Response({'error': 'email and team_name is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            mentor = Team.objects.get(mentor__email=email, team_name=team_name)
            if mentor is not None:
                serializer = TeamSerializer(mentor) # use many=False to serialize a single object
                return Response(serializer.data)
            else:
                return Response({'error': 'Record not found'},status=status.HTTP_404_NOT_FOUND)
        except Team.DoesNotExist: 
            return Response({"error": "You are not a mentor of this team (or) record not found"},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Record not found'},status=status.HTTP_404_NOT_FOUND)


    def put(self, request, format=None):
        logging.info(request.data)
        email = request.query_params.get('email')
        team_name = request.query_params.get('team_name')
        if not email or not team_name:
            return Response({'error': 'email and team_name is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            team = Team.objects.get(mentor__email=email, team_name=team_name)
            if team is not None:
                # Check if the request user email matches the team mentor email
                serializer = TeamSerializer(team, data=request.data)
                if serializer.is_valid():
                    serializer.save(update_fields=["project", "mentor","members"])
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Record not found'},status=status.HTTP_404_NOT_FOUND)
        except Team.DoesNotExist: 
            return Response({"error": "You are not a mentor of this team (or) record not found"},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Record not found'},status=status.HTTP_404_NOT_FOUND)



    def post(self, request, format=None):
        logging.info(request.data)
        team_name = request.data.get('team_name')
        if Team.objects.filter(team_name=team_name).exists(): 
            return Response({'error': 'The team name is already taken'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = TeamSerializer(data=request.data) 
            if serializer.is_valid():
                serializer.save()
                return Response({"success":"The team was created successfully","Record":serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        



class MentorAPIView(APIView):
    """
    View to get all courses,projects,teams,team members data based on email
    """ 
    permission_classes = [IsAuthenticated]

    def get_object(self):
        email = self.request.query_params.get('email')
        user = None
        if email is not None:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None
        return user


    def get(self, request, format=None):
        user = self.get_object()
        # logging.info(user)
        if user is not None:
            data = {"team_mentor_info": [],"courses": []}
            data["team_mentor_info"] = {
                "id":user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role":user.role,
                "course_id": user.course_id,
                "college": user.college.college_name
            }

            courses = (user.course_id).split(",")
            # logging.info(courses)
            for course in courses:
                course = course.strip()
                courses = Project.objects.filter(college=user.college,course_id=course).values_list("course_id", flat=True).distinct()
                # logging.info(courses)
                for course in courses:
                    course_name = Project.objects.filter(course_id=course).first().course_name
                    # get the course name from the Course model 
                    projects = Project.objects.filter(college=user.college, course_id=course)               
                    course_data = {"course_id": course, "course_name": course_name, "projects": [],"unassigned_members": []} # create a dictionary for each course 
                    for project in projects:
                        teams = Team.objects.filter(project=project)
                        project_data = {"id": project.id, "project_name": project.project_name, "project_description": project.project_description, "teams_count": 0, "teams": []} # create a dictionary for each project 
                        # add a teams_count key to the project data and initialize it to zero
                        for team in teams:
                            members = team.members.all()
                            seats_filled = len(team.members.all()) + 1
                            seats_available = int(user.college.team_size) - seats_filled
                            mentor = team.mentor.email
                            # mentor = [team.mentor.email]
                            # mentors = User.objects.filter(role="Team Mentor", course_id__contains=course,college=user.college)
                            # mentor_emails = mentors.values_list('email', flat=True)
                            # new_list = mentor + [x for x in mentor_emails if x not in mentor]
                            # logging.info(new_list)
                            team_data = { "team_id": team.id, "team_name": team.team_name, "team_mentor": mentor, "team_size": user.college.team_size, "seats_filled": seats_filled, "seats_available": seats_available, "team_members": [member.email for member in members] } # create a dictionary for each team 
                            project_data["teams"].append(team_data)
                            project_data["teams_count"] += 1 # increment the teams_count by one for each team
                        course_data["projects"].append(project_data)
                    data["courses"].append(course_data) 


                all_members = User.objects.filter(Q(role="Team member") | Q(role="Team Member"),course_id=course,college=user.college)
                #logging.info(all_members)
                assigned_members = set()
                for course in data["courses"]:
                    for project in course["projects"]:
                        for team in project["teams"]:
                            for member in team["team_members"]:
                                assigned_members.add(member)

                for member in all_members:
                    if member.email not in assigned_members and member.email:
                        course_data["unassigned_members"].append(member.email)

            return JsonResponse(data, safe=False) 
        else:
            return JsonResponse({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        


class SpocAPIView(APIView):
    " View to display Mentors and evaluator information for Spoc and also to add,update the mentors/spocs to the spoc dashboard."

    def get_object(self):
        email = self.request.query_params.get('email')
        user = None
        if email is not None:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None
        return user

    def get(self,request, format= None):
        user = self.get_object()
        if user and user.role == "Spoc":
            spoc = User.objects.get(email=user.email, role__in=["Principal", "Spoc"])
            college = spoc.college
            total_students_count = User.objects.filter(college=college,role="Team Member").count()
            total_students_registered_count= User.objects.filter(college=college, role="Team Member", enrollment__is_registered=True).count()
            data = {"info": [],"mentors_and_evals": []}
            data["info"] = {
                           
                "college": user.college.college_name,
                "total_students": total_students_count,
                "total_students_registered": total_students_registered_count,
                "total_students_unregistered": total_students_count - total_students_registered_count

            }

            mentors_and_evals_list = User.objects.filter(college=college, role__in=["Team Mentor", "Evaluator"])
            for member in mentors_and_evals_list:
                # Append each member's data to the list
                data["mentors_and_evals"].append({

                    "email": member.email,
                    "first_name": member.first_name,
                    "last_name": member.last_name,
                    "role": member.role,
                    "course_id": member.course_id,
                    "college": member.college.college_name,
                    "branch": member.branch,
                    "technology": member.technology
                })
            # Return the response after the loop
            return JsonResponse(data, safe=False) 
        else:
            return JsonResponse({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # def put(self, request, format=None):
    #     email = request.query_params.get('email')
    #     if not email:
    #         return Response({'error': 'email is required'}, status=status.HTTP_400_BAD_REQUEST)
    #     try:
    #         user = self.get_object()
    #         serializer = UserSerializer(user, data=request.data, partial=True)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_200_OK)
    #         else:
    #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     except User.DoesNotExist: # Assuming self.model is the user model
    #         return Response({'error': 'user does not exist'}, status=status.HTTP_404_NOT_FOUND)
    #     except Exception as e: # Catch any other exception
    #         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        

    def put(self, request, format=None):
            email = request.query_params.get('email')
            if not email:
                return Response({'error': 'email is required'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                user = User.objects.get(email=email)
                technology = request.data.get('technology')
                branch = request.data.get('branch')
                new_email = request.data.get('email')
                first_name = request.data.get('first_name')
                last_name = request.data.get('last_name')
                update_fields = {}
                if technology:
                    update_fields['technology'] = technology
                if branch:
                    update_fields['branch'] = branch
                if new_email:
                    update_fields['email'] = new_email
                if first_name:
                    update_fields['first_name'] = first_name
                if last_name:
                    update_fields['last_name'] = last_name
                rows_updated = User.objects.filter(email=email).update(**update_fields)
                if rows_updated > 0:
                    user = User.objects.get(email=new_email or email)
                    data = model_to_dict(user)
                    return Response({"success":"The user data was updated successfully","Record":data}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'no user was updated'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({'error': 'user does not exist'}, status=status.HTTP_404_NOT_FOUND)

            
    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        if user is not None:
            new_role = request.data.get("role")
            if new_role in ["", "None", "Team Member", "Team Mentor", "Spoc", "Evaluator", "Principal", "Admin"]:
                user.role = new_role
                user.save()
                data = {"email": user.email,"role": user.role}
                return Response({"success":"The user role was deleted successfully","Record":data}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # def post(self, request, format=None):
    #     # logging.info(request.data)
    #     email = request.data.get('email')
    #     if User.objects.filter(email=email).exists(): 
    #         return Response({'error': 'User is already exist'}, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         serializer = UserSerializer(data=request.data) 
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response({"success":"The user was created successfully","Record":serializer.data}, status=status.HTTP_201_CREATED)
    #         else:
    #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request, format=None):
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        college = request.data.get('college')
        role = request.data.get('role')
        branch = request.data.get('branch')
        technology = request.data.get('technology')
        try:
            if User.objects.filter(email=email).exists(): 
                return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user_data = {
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name,
                    "college": college,
                    "role": role,
                    "branch": branch,
                    "technology": technology
                }
                serializer = UserSerializer(data=user_data) 
                if serializer.is_valid():
                    serializer.save()
                    return Response({"success":"The user was created successfully","Record":serializer.data}, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"An error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            print("API call finished")





class OverallDashboardAPIView(APIView):
    " View to display some statistics based on the models."

    def get(self, request, format=None):

        try:
            spocs_count = User.objects.filter(role="Spoc").count()
            mentors_count = User.objects.filter(role="Team Mentor").count()
            eval_count = User.objects.filter(role="Evaluator").count()
            mentor_eval_count = User.objects.filter(Q(role="Team Mentor") & Q(is_evaluator=True)).count()
            evaluators_count = eval_count + mentor_eval_count
            college_count = College.objects.count()
            team_member_count = User.objects.filter(role="Team Member").count()
            # logging.info(team_member_count)
            # students_registered = TnsdcEnrollment.objects.filter(is_registered=True).values("email").distinct().count()
            students_registered_data = TnsdcEnrollment.objects.filter(is_registered=True).values_list("email__email",flat=True).distinct()
            # logging.info(students_registered_data)
            students_registered = User.objects.filter(email__in=students_registered_data, role="Team Member").count()
            # logging.info(students_registered)
            # Get the distinct course ids from the user model
            course_ids = User.objects.filter(role="Team Member").values_list("course_id", flat=True).distinct()

            coursewise_students = []

            for course_id in course_ids:
                # Get the course name from the project model
                project = Project.objects.filter(course_id=course_id).first()
                if project:
                    course_name = project.course_name
                    student_count = User.objects.filter(role="Team Member", course_id=course_id).count()
                    coursewise_students.append({
                        "course_id":course_id,
                        "course_name": course_name,
                        "student_count": student_count
                    })
                else:
                    pass

            response_data = {
                "Total_students": team_member_count,
                "registered_students": students_registered,
                "Total_colleges": college_count,
                "Total_Spocs": spocs_count,
                "Total_Mentors": mentors_count,
                "Total_Evaluators": evaluators_count,
                "coursewise_students": coursewise_students
            }
        except ObjectDoesNotExist as e:
            print(e)
            return Response({"error": "Object does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except MultipleObjectsReturned as e:
            print(e)
            return Response({"error": "Multiple objects returned"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            print("API executed successfully")
            return Response(response_data)
        finally:
            pass








class PrincipalDashboardAPIView(APIView):
    ''' A view that returns the statistics for a principal based on their email. '''
    def get(self, request):
        email = request.query_params.get("email", None)
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            principal = User.objects.get(email=email, role__in=["Principal", "Spoc"])
            # principal = User.objects.get(email=email, Q(role="Principal") | Q(role="Spoc"))
        except User.DoesNotExist:
            return Response({"error": "Principal not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            college = principal.college
            college_name = principal.college.college_name
            # total_students_registered = User.objects.filter(college=college, role="Team Member", is_registered=True).count()
            total_students = User.objects.filter(college=college,role="Team Member").count()
            total_students_registered = User.objects.filter(college=college, role="Team Member", enrollment__is_registered=True).count()
            total_students_enrolled = User.objects.filter(college=college, role="Team Member", enrollment__is_registered=True).count()
            total_teams_created = Team.objects.filter(members__college=college).distinct().count()
            total_projects_assigned = Project.objects.filter(college=college).count()
            total_spoc_registered = User.objects.filter(college=college, role="Spoc", enrollment__is_registered=True).count()
            total_spoc_enrolled = User.objects.filter(college=college, role="Spoc", enrollment__is_registered=True).count()
            total_mentors_registered = User.objects.filter(college=college, role="Team Mentor", enrollment__is_registered=True).count()
            total_mentors_enrolled = User.objects.filter(college=college, role="Team Mentor", enrollment__is_registered=True).count()
            total_evaluators_registered = User.objects.filter(college=college, role="Evaluator", enrollment__is_registered=True).count()
            total_evaluators_enrolled = User.objects.filter(college=college, role="Evaluator", enrollment__is_registered=True).count()

            data = {
                "college_name": college_name,
                "Total_students": total_students,
                "students_registered": total_students_registered,
                "students_enrolled": total_students_enrolled,
                "teams_created": total_teams_created,
                "projects_assigned": total_projects_assigned,
                "spocs_registered": total_spoc_registered,
                "spocs_enrolled": total_spoc_enrolled,
                "mentors_registered": total_mentors_registered,
                "mentors_enrolled": total_mentors_enrolled,
                "evaluators_registered": total_evaluators_registered,
                "evaluators_enrolled": total_evaluators_enrolled,
            }


            college_code = college.college_id
            try:
                spoc = User.objects.get(college=college, role="Spoc")
                spoc_name = str(spoc.first_name) + " " + str(spoc.last_name)
            except User.DoesNotExist:
                spoc = None
                spoc_name = None

            users = User.objects.filter(college=college, role="Team Member")
            team_data = []
            for user in users:
                email = user.email
                logging.info(email)
                course = user.course_id
                project = Project.objects.filter(course_id=course).first()
                if project is None:
                    course_name = None
                else:
                    course_name = project.course_name
                registered = None
                # Check if the user is registered and enrolled in the course
                registered = TnsdcEnrollment.objects.filter(Q(email=user) & Q(course_id=course) & Q(is_enrolled=True) & Q(is_registered=True)).exists()
                logging.info(registered)
                # registered = bool_to_yes_no(registered_students)
                team = Team.objects.filter(members__email=email).first()
                if team is None:
                    team_id = None
                    mentor_name = None
                    evaluator_name = None
                    project_name = None
                    
                else:
                    team_id = team.id
                    mentor = team.mentor
                    if mentor is None:
                        mentor_name = None
                    else:
                        # mentor_name = mentor.__str__()
                        mentor_name = str(team.mentor.first_name) + " " + str(team.mentor.last_name)
                    evaluator = team.evaluator
                    if evaluator is None:
                        evaluator_name = None
                    else:
                        # evaluator_name = evaluator.__str__()
                        evaluator_name = str(team.evaluator.first_name) + " " + str(team.evaluator.last_name)
                    project = team.project 
                    if project is None:
                        project_name = None
                    else:
                        project_name = project.project_name


                team_data.append({
                    "team_id": team_id,
                    "email": user.email,
                    "student_name": str(user.first_name) + " " + str(user.last_name),
                    "nm_id": user.nm_id,
                    "course_id": user.course_id,
                    "course_name": course_name,
                    "mentor_name": mentor_name,
                    "evaluator_name": evaluator_name,
                    "project_allotted" : project_name,
                    "registered" : registered                 
                    
                })

                user_data = {
                    "college_name": college_name,
                    "college_code": college_code,
                    "spoc_name": spoc_name,
                    "team_data": team_data
                }
                data.update({"user_data": user_data})

            # return JsonResponse(data)
        except ObjectDoesNotExist as e:
            print(e)
            return Response({"error": "Object does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except MultipleObjectsReturned as e:
            print(e)
            return Response({"error": "Multiple objects returned"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            print("API executed successfully")
            return JsonResponse(data)
        finally:
            pass





class MentorDashboardAPIView(APIView):


    def get(self, request, format=None):

        email = request.query_params.get("email", None)
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            mentor = User.objects.get(email=email, role="Team Mentor")
        except User.DoesNotExist:
            return Response({"error": "Mentor not found"}, status=status.HTTP_404_NOT_FOUND)
        if mentor is not None:
            try:
                data = {"courses": []}

                college = mentor.college
                college_details = College.objects.get(college_name=college)
                college_id = college_details.college_id
                college_name = mentor.college.college_name
                # students_registered = User.objects.filter(college=college, role="Team Member").count()
                # students_registered = TnsdcEnrollment.objects.filter(email__college=college, is_registered=True).count()
                students_registered = TnsdcEnrollment.objects.filter(email__college=college, is_registered=True).values("email").distinct().count()
                students_enrolled = TnsdcEnrollment.objects.filter(email__college=college, is_enrolled=True).count()
                teams_created = Team.objects.filter(members__college=college,mentor__email=email).distinct().count()
                projects_assigned = Project.objects.filter(college=college).count()
                students_unassigned = User.objects.filter(college=college, role="Team Member", teams_members=None).count()
                projects_evaluated = Team.objects.filter(evaluator=mentor).count()

                teams_created_by_mentor = Team.objects.filter(mentor=mentor).count()
                # teams_created_by_mentor_serializer = TeamSerializer(teams_created_by_mentor, many=True)
                email = mentor.email
                projects_allotted = Team.objects.filter(mentor__email=email).values("project").distinct().count()
                data ={
                    "college_name": college_name,
                    "college_id" : college_id,
                    "students_registered": students_registered,
                    "students_enrolled": students_enrolled,
                    "teams_created": teams_created,
                    "projects_assigned": projects_assigned,
                    "students_left_unassigned": students_unassigned,
                    "projects_evaluated_by_mentor": projects_evaluated,
                    "teams_created_by_mentor": teams_created_by_mentor,
                    "projects_allotted_to_mentor": projects_allotted,
                }
                # logging.info(college)
                courses = (mentor.course_id).split(",")
                # logging.info(courses)
                for course in courses:
                    course = course.strip()
                    courses = Project.objects.filter(college=college,course_id=course).values_list("course_id", flat=True).distinct()
                    # logging.info(courses)
                    for course in courses:
                        course_name = Project.objects.filter(course_id=course).first().course_name
                        # get the course name from the Course model 
                        # projects = Project.objects.filter(college=college, course_id=course)
                        projects = Project.objects.filter(college=college, course_id=course, team__isnull=False,team__mentor__email=email).distinct()
                        # logging.info(projects)              
                        course_data = {"course_id": course, "course_name": course_name, "projects": []} # create a dictionary for each course 
                        for project in projects:
                            # teams = Team.objects.filter(project=project,mentor__email=mentor)
                            # logging.info(teams)
                            # for team in teams:
                            #     project_data = {"id": team.project.id, "project_name": team.project.project_name, "teams": []}
                            #     members = team.members.all()
                            #     # logging.info(members)
                            #     team_data = { "team_id": team.id, "team_name": team.team_name,"team_members": [] }
                            #     logging.info(team_data)
                            #     for member in members: # loop through each member and get their details from the User model
                            #         user = User.objects.get(email=member.email) # get the user object by email
                            #         member_data = { "email": user.email, "first_name": user.first_name, "last_name": user.last_name, "nm_id": user.nm_id } # create a dictionary for each member with their details
                            #         team_data["team_members"].append(member_data) # append the member data to the team data
                            #     project_data["teams"].append(team_data)
                            # course_data["projects"].append(project_data)

                            # get all the teams for this project using prefetch_related
                            teams = project.team_set.prefetch_related('members').filter(mentor__email=email)
                            # create a dictionary for this project
                            project_data = {"id": project.id, "project_name": project.project_name, "teams": []}
                            for team in teams:
                                # create a dictionary for this team
                                team_data = { "team_id": team.id, "team_name": team.team_name,"team_members": [] }
                                # get only the fields you need from the members using values
                                members = team.members.values('email', 'first_name', 'last_name', 'nm_id')
                                for member in members:
                                    member_data = { "email": member['email'], "first_name": member['first_name'], "last_name": member['last_name'], "nm_id": member['nm_id'] }
                                    team_data["team_members"].append(member_data)
                                project_data["teams"].append(team_data)
                            course_data["projects"].append(project_data)
                        if 'user_data' not in data:
                            data['user_data'] = []
                        data['user_data'].append(course_data)


                # return JsonResponse(data, safe=False) 
            except ObjectDoesNotExist as e:
                print(e)
                return Response({"error": "Object does not exist"}, status=status.HTTP_404_NOT_FOUND)
            except MultipleObjectsReturned as e:
                print(e)
                return Response({"error": "Multiple objects returned"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(e)
                return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                print("API executed successfully")
                return JsonResponse(data)
            finally:
                pass








class AdminBasedDashboardAPIView(APIView):
    '''A view that returns the user data based on the role query parameter. '''

    def get(self, request, format=None):
        role = request.query_params.get("role", None)
        if role is None:
            return Response({"error": "Role is required"}, status=400)
        if role not in ["Team Mentor", "Evaluator", "Spoc"]:
            return Response({"error": "Invalid role"}, status=404)
        try:
            users = User.objects.filter(role=role)
            if role == "Evaluator":
                evaluators = User.objects.filter(Q(role="Team Mentor") & Q(is_evaluator=True))
                users = users | evaluators # Union of two querysets
            # logging.info(users)

            user_data = []
            for user in users:
                college = user.college
                course_id = user.course_id
                # Split the course_id by commas and loop through each one
                course_names = []
                for cid in course_id.split(","):
                    cid = cid.strip()
                    project = Project.objects.filter(course_id=cid).first() # Get the first matching project or None
                    if project is not None:
                        course_name = project.course_name 
                        course_names.append(course_name)
                    else:
                        logging.error(f"No project found with course_id {cid}")

                course_names = ", ".join(course_names)

                data = {
                    "nm_id": user.nm_id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "college_code": college.college_id,
                    "college_name": college.college_name,
                    "course_id": course_id,
                    "course_name": course_names,
                }
                user_data.append(data)

            count = len(user_data)

            # return Response({"count": count, "user_data": user_data})
        except ObjectDoesNotExist as e:
            print(e)
            return Response({"error": "Object does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except MultipleObjectsReturned as e:
            print(e)
            return Response({"error": "Multiple objects returned"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            print("API executed successfully")
            return Response({"count": count, "user_data": user_data})
        finally:
            pass




class CollegeRoleDashboardAPIView(APIView):
    '''A view that returns the user data based on the role and college name query parameters. '''


    def get(self, request, format=None):
        role = request.query_params.get("role", None)
        college_name = request.query_params.get("college_name", None)
        if role is None:
            return Response({"error": "Role is required"}, status=400)
        if role not in ["Team Mentor", "Evaluator", "Spoc"]:
            return Response({"error": "Invalid role"}, status=404)
        try:
            if college_name is None:
                users = User.objects.filter(role=role)
            else:
                users = User.objects.filter(role__iexact=role, college__college_name__iexact=college_name)
            if role == "Evaluator":
                evaluators = User.objects.filter(Q(role="Team Mentor") & Q(is_evaluator=True))
                if college_name is not None: # Filter evaluators by college name
                    evaluators = evaluators.filter(college__college_name__iexact=college_name)
                users = users | evaluators # Union of two querysets

            user_data = []
            # for user in users:
            #     college = user.college
            #     course_id = user.course_id
            #     logging.info(user)
            #     logging.info(course_id)
                # course_name = Project.objects.filter(course_id=course_id).first().course_name
            for user in users:
                college = user.college
                course_id = user.course_id
                course_names = []
                for cid in course_id.split(","):
                    cid = cid.strip()
                    project = Project.objects.filter(course_id=cid).first() 
                    if project is not None: 
                        course_name = project.course_name 
                        course_names.append(course_name)
                    else: # Handle the case when project is None
                        logging.error(f"No project found with course_id {cid}")

                course_names = ", ".join(course_names)

                data = {
                    "nm_id": user.nm_id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "college_code": college.college_id,
                    "college_name": college.college_name,
                    "course_id": course_id,
                    # "course_name": Project.objects.get(course_id=course_id).course_name,
                    "course_name": course_names,
                }
                user_data.append(data)

            count = len(user_data)

            # return Response({"count": count, "user_data": user_data})
        except ObjectDoesNotExist as e:
            print(e)
            return Response({"error": "Object does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except MultipleObjectsReturned as e:
            print(e)
            return Response({"error": "Multiple objects returned"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            print("API executed successfully")
            return Response({"count": count, "user_data": user_data})
        finally:
            pass


class AllCollegesDashboardAPIView(APIView):
    def get(self, request, format=None):
        college_name = request.query_params.get('college_name')
        if college_name is not None:
            colleges = College.objects.filter(college_name=college_name)
        else:
            colleges = College.objects.all()

        data = []
        for college in colleges:
            college_code = college.college_id
            college_name = college.college_name

            # Get the number of students from that college by counting the users with that college foreign key
            number_of_students = User.objects.filter(college=college).count()

            college_data = {
                'college_code': college_code,
                'college_name': college_name,
                'number_of_students': number_of_students
            }
            data.append(college_data)

        data = {'count': len(data), 'user_data': data}
        return Response(data, status=status.HTTP_200_OK)



class PhasewiseSubmissionAPIView(APIView):
    def get(self, request, format=None):
        email = request.query_params.get("email",None)
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "user not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            if user.role == "Admin":
                submissions = []
                colleges = College.objects.all()
                for college in colleges:
                    college_name = college.college_name
                    total_students = User.objects.filter(college=college,role="Team Member").count()
                    phase_one_submissions = TnsdcSubmission.objects.filter(college=college, phase1_submitted=True).count()
                    phase_one_evaluations_one = TnsdcSubmission.objects.filter(college=college, eval1_p1__gt=0).count()
                    phase_one_evaluations_two = TnsdcSubmission.objects.filter(college=college, eval2_p1__gt=0).count()
                    phase_two_submissions = TnsdcSubmission.objects.filter(college=college, phase2_submitted=True).count()
                    phase_two_evaluations_one = TnsdcSubmission.objects.filter(college=college, eval1_p2__gt=0).count()
                    phase_two_evaluations_two = TnsdcSubmission.objects.filter(college=college, eval2_p2__gt=0).count()
                    phase_three_submissions = TnsdcSubmission.objects.filter(college=college, phase3_submitted=True).count()
                    phase_three_evaluations_one = TnsdcSubmission.objects.filter(college=college, eval1_p3__gt=0).count()
                    phase_three_evaluations_two = TnsdcSubmission.objects.filter(college=college, eval2_p3__gt=0).count()
                    phase_four_submissions = TnsdcSubmission.objects.filter(college=college, phase4_submitted=True).count()
                    phase_four_evaluations_one = TnsdcSubmission.objects.filter(college=college, eval1_p4__gt=0).count()
                    phase_four_evaluations_two = TnsdcSubmission.objects.filter(college=college, eval2_p4__gt=0).count()
                    phase_five_submissions = TnsdcSubmission.objects.filter(college=college, phase5_submitted=True).count()
                    phase_five_evaluations_one = TnsdcSubmission.objects.filter(college=college, eval1_p5__gt=0).count()
                    phase_five_evaluations_two = TnsdcSubmission.objects.filter(college=college, eval2_p5__gt=0).count()
                    final_submissions = TnsdcSubmission.objects.filter(college=college, final_submission=True).count()
                    college_data = {
                        "id": college.id,
                        "college_name": college_name,
                        "Total_students":total_students,
                        "phase_one_submission": phase_one_submissions,
                        "phase_one_evaluation_one": phase_one_evaluations_one,
                        "phase_one_evaluation_two": phase_one_evaluations_two,
                        "phase_two_submission": phase_two_submissions,
                        "phase_two_evaluation_one": phase_two_evaluations_one,
                        "phase_two_evaluation_two": phase_two_evaluations_two,
                        "phase_three_submission": phase_three_submissions,
                        "phase_three_evaluation_one": phase_three_evaluations_one,
                        "phase_three_evaluation_two": phase_three_evaluations_two,
                        "phase_four_submission": phase_four_submissions,
                        "phase_four_evaluation_one": phase_four_evaluations_one,
                        "phase_four_evaluation_two": phase_four_evaluations_two,
                        "phase_five_submission": phase_five_submissions,
                        "phase_five_evaluation_one": phase_five_evaluations_one,
                        "phase_five_evaluation_two": phase_five_evaluations_two,
                        "final_submission" : final_submissions
                    }
                    submissions.append(college_data)
                response_data = {
                    "submissions": submissions
                }
                return Response(response_data)
            elif user.role == "Principal":
                submissions = User.objects.filter(college=user.college).select_related("submission").annotate(college_name=F('college__college_name'),
                            phase_one_submission=F('submission__phase1_submitted'),phase_one_evaluation_one=F('submission__eval1_p1'),phase_one_evaluation_two=F('submission__eval2_p1'),
                            phase_two_submission=F('submission__phase2_submitted'),phase_two_evaluation_one=F('submission__eval1_p2'),phase_two_evaluation_two=F('submission__eval2_p2'),
                            phase_three_submission=F('submission__phase3_submitted'),phase_three_evaluation_one=F('submission__eval1_p3'),phase_three_evaluation_two=F('submission__eval2_p3'),
                            phase_four_submission=F('submission__phase4_submitted'),phase_four_evaluation_one=F('submission__eval1_p4'),phase_four_evaluation_two=F('submission__eval2_p4'),
                            phase_five_submission=F('submission__phase5_submitted'),phase_five_evaluation_one=F('submission__eval1_p5'),phase_five_evaluation_two=F('submission__eval2_p5'),
                            final_submission=F('submission__final_submission'),final_marks=F('submission__final_marks')).values("nm_id","email","college_name","course_id",
                                        "phase_one_submission","phase_one_evaluation_one","phase_one_evaluation_two",
                                        "phase_two_submission","phase_two_evaluation_one","phase_two_evaluation_two",
                                        "phase_three_submission","phase_three_evaluation_one","phase_three_evaluation_two",
                                        "phase_four_submission","phase_four_evaluation_one","phase_four_evaluation_two",
                                        "phase_five_submission","phase_five_evaluation_one","phase_five_evaluation_two",
                                        "final_submission","final_marks")
                student_submissions = list(submissions) 
                response_data = { "submissions": student_submissions } 
                return Response(response_data) 
            elif user.role == "Team Mentor":
                teams = Team.objects.filter(mentor__email=email)
                submissions = [] 

                for team in teams: 
                    members = team.members.all()
                    for member in members:
                        # Use select_related to join User and TnsdcSubmission models
                        member_details = User.objects.filter(email=member).select_related("submission").annotate(college_name=F('college__college_name'),
                                        phase_one_submission=F('submission__phase1_submitted'),phase_one_evaluation_one=F('submission__eval1_p1'),phase_one_evaluation_two=F('submission__eval2_p1'),
                                        phase_two_submission=F('submission__phase2_submitted'),phase_two_evaluation_one=F('submission__eval1_p2'),phase_two_evaluation_two=F('submission__eval2_p2'),
                                        phase_three_submission=F('submission__phase3_submitted'),phase_three_evaluation_one=F('submission__eval1_p3'),phase_three_evaluation_two=F('submission__eval2_p3'),
                                        phase_four_submission=F('submission__phase4_submitted'),phase_four_evaluation_one=F('submission__eval1_p4'),phase_four_evaluation_two=F('submission__eval2_p4'),
                                        phase_five_submission=F('submission__phase5_submitted'),phase_five_evaluation_one=F('submission__eval1_p5'),phase_five_evaluation_two=F('submission__eval2_p5'),
                                        final_submission=F('submission__final_submission'),final_marks=F('submission__final_marks')).values("nm_id","email","college_name","course_id",
                                        "phase_one_submission","phase_one_evaluation_one","phase_one_evaluation_two",
                                        "phase_two_submission","phase_two_evaluation_one","phase_two_evaluation_two",
                                        "phase_three_submission","phase_three_evaluation_one","phase_three_evaluation_two",
                                        "phase_four_submission","phase_four_evaluation_one","phase_four_evaluation_two",
                                        "phase_five_submission","phase_five_evaluation_one","phase_five_evaluation_two",
                                        "final_submission","final_marks")
                        submissions.append(member_details)
                        response_data = {"submissions": submissions}
        #     return Response(response_data)    
        # else:
        #     return Response({"error": "You are not authorized to access this data."})

        except ObjectDoesNotExist as e:
            print(e)
            return Response({"error": "Object does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except MultipleObjectsReturned as e:
            print(e)
            return Response({"error": "Multiple objects returned"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            print("API executed successfully")
            return Response(response_data)
        finally:
            pass
   

