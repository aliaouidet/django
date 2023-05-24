import random
import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from service.models import (
    User,
    Project,
    Service,
    ProjectService,
    Team,
    TeamMember,
    ProjectFile,
    Testimonial,
    Article,
    Comment,
)

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates sample projects'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of sample projects to be created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        clients = User.objects.filter(is_superuser=False)
        services = Service.objects.all()
        teams = Team.objects.all()

        for i in range(total):
            title = f'Sample Project {i+1}'
            description = f'This is the description for Sample Project {i+1}'
            start_date = timezone.now().date()
            end_date = start_date + timedelta(days=30)
            client = clients[i % len(clients)]
            assigned_team = teams[i % len(teams)]

            project = Project.objects.create(
                title=title,
                description=description,
                start_date=start_date,
                end_date=end_date,
                client=client,
                assigned_team=assigned_team,
            )

            # Assign random services to the project
            project_services = services.order_by('?')[:3]
            for service in project_services:
                ProjectService.objects.create(project=project, service=service)

            # Create team members
            members = TeamMember.objects.filter(team=assigned_team)
            for member in members:
                if member.is_leader:
                    leader = member.member
                    break

            # Create project files with images from API
            for j in range(3):
                file_type = random.choice(['IMG'])
                image_url = f'https://api.example.com/images/{file_type.lower()}_file{j+1}'
                response = requests.get(image_url)

                if response.status_code == 200:
                    file_name = f'{file_type.lower()}_file{j+1}'
                    file_content = ContentFile(response.content)

                    project_file = ProjectFile.objects.create(
                        project=project,
                        file_type=file_type,
                        file=file_content,
                    )
                    project_file.file.save(file_name, file_content, save=True)

            # Create testimonials
            testimonial = Testimonial.objects.create(
                project=project,
                author_name=f'Testimonial Author {i+1}',
                author_company=f'Testimonial Company {i+1}',
                text=f'Testimonial text for Sample Project {i+1}',
            )

            # Create articles
            article = Article.objects.create(
                title=f'Sample Article {i+1}',
                content=f'Content of Sample Article {i+1}',
                author=leader,
            )

            # Create comments
            for j in range(3):
                Comment.objects.create(
                    project=project,
                    user=clients[(i + j) % len(clients)],
                    text=f'Comment text {j+1} for Sample Project {i+1}',
                )

            self.stdout.write(self.style.SUCCESS(f'Successfully created project "{title}"'))
