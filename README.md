\# EzyHelpers



EzyHelpers is a helper job-management application built with Flutter and Django REST Framework.



\## Features



\- Helper login using the Django REST API

\- View assigned jobs and job details

\- Update job status: `ASSIGNED` → `IN\_PROGRESS` → `COMPLETED`

\- Backend job ownership enforcement

\- Firebase Analytics events: `login\_success`, `job\_viewed`, `job\_status\_updated`

\- Django Admin for managing and assigning jobs



\## Technology Stack



\- \*\*Mobile:\*\* Flutter and Dart

\- \*\*Backend:\*\* Django and Django REST Framework

\- \*\*Database:\*\* SQLite

\- \*\*Analytics:\*\* Firebase Analytics



\## Project Structure



```text

EzyHelpers/

├── backend/

│   ├── config/

│   ├── jobs/

│   ├── manage.py

│   └── requirements.txt

├── mobile/

│   ├── android/

│   ├── lib/

│   └── pubspec.yaml

└── README.md

```



\## Backend Setup



Run these commands from the repository root in PowerShell.



Install the dependencies:



```powershell

py -m pip install -r backend\\requirements.txt

```



Set a development secret:



```powershell

$env:DJANGO\_SECRET\_KEY = py -c "from django.core.management.utils import get\_random\_secret\_key; print(get\_random\_secret\_key())"

```



Run database migrations:



```powershell

py backend\\manage.py migrate

```



Create an administrator:



```powershell

py backend\\manage.py createsuperuser

```



Start the backend:



```powershell

py backend\\manage.py runserver 0.0.0.0:8000

```



Django Admin is available at `/admin/`.



\## Mobile App Setup



Install Flutter dependencies:



```powershell

cd mobile

flutter pub get

```



Configure the API base URL in `lib/services/api\_service.dart` to use your computer's LAN IP address and port `8000`, for example:



`http://YOUR\_COMPUTER\_LAN\_IP:8000/api`



Connect your Android device and computer to the same network, then run:



```powershell

flutter devices

flutter run

```



Configure Firebase for the app before using Firebase Analytics.



\## Job Workflow



1\. An administrator assigns a job to a helper.

2\. The helper logs in.

3\. The helper views assigned jobs and opens job details.

4\. The helper updates the job status through the supported workflow.



The backend validates job ownership and status transitions.



\## Tests



Run backend tests from the repository root:



```powershell

py backend\\manage.py test jobs

```



Run Flutter analysis and tests:



```powershell

cd mobile

flutter analyze

flutter test

```



\## Security



\- Never commit passwords, private credentials, or Django secret keys.

\- Configure `DJANGO\_SECRET\_KEY` in each local development session.

\- Use HTTPS and production security settings for deployed environments.

\- The local development server is not intended for production use.



\## Repository



Source code for the Flutter app and Django backend is maintained in this repository.

