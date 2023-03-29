# TicketBooking

## Folder structure

    ├── application
    ├	├── api		    		# CRUD operations
    ├	└── controllers			# controllers
    ├── instances				# database file
    ├── models			    	# database table model
    ├── static				    # generated matplotlib graph
    ├── template
    ├	├── admin   			# admin html file
    ├	├── login				# user html file
    ├	├── registration		# registration html file
    ├	└── user				# user html file
    ├── app.py		    		# main file, app beginning
    ├── api.yaml				# api documentation file
    ├── project Documentation	# project Documentation
    ├── README.md				# few applications rule
    └── requirement.txt			# required packages

## Available packages used

    - datetime
    - random
    - string
    - sqlite3
    - re
    - os

## Aditional Packages Downloaded

    - Flask
    - Flask-SQLAlchemy
    - Flask-RESTful
    - Flask-Cors
    - Flask-Login
    - jinja2
    - matplotlib
    - pandas

## Installation

Install all the additional package with help of below command

```bash
pip install packageName
```

## Running project

Since I had used virtual environment, I will activate virtual environment and I will eun the projext

```bash
virenv/scripts/activate
python app.py
```

## User View

### Bookings

    User can book any number of tickets of show subject to availability
    Bookings will disabled if ticket sold for the show
    The allocation will be hidden from the homepage if start time passes the current time

### Ticket Fare calculation

    Both venue and show will have separate fare details
    Application will pick up the maximum of venue fare or Show fare and uses it during booking according to 2D or 3D movie

### Search

    User can search using 6 different parameter as follows
    - Search by Venue Name
    - Search by Venue Location
    - Search by Show Name
    - Search by Show Tags
    - Search by Show Ratings`
    - Search allocation by date

### Rating

    A user can can Rate a show on scale 1 to 5.
    A user can rate a show only once despite the number of booking on same shows in different venues

### Reset Password

    User can reset his/her password

## Admin View

    Admin can create or edit or delete Show, Venue and allocation details
    Venues and shows cannot be deleted unless their allocation is deleted

### Admin Registration

    Admin can register only if he/she has vaild admin code
    The admin code is genrated by current admin in his/her profile page
    This is kind of security that blocks anyone come register, login and edit the show

### Allocation constaraints

    Admin can create allocation after 15 mins from current time
    Admin can edit, delete and view the details of allocation
    Allocation are taken care like there should be 15 min break between end of one show and beggining of next show

### Archive

    Admin can view the past shows in the archive page
    These show details can be view or deleted but it is not possible to edit the past shows

### Show Constraints

    We cannot create two show under same name
    Admin can type one or more tags separated by semicolon(;)
    Admin can choose whether show is 2D/3D while creating and editing

### Venue Constraints

    There can not be two venue name with same location
    There can be same venue name if location are different
    If user try to edit a venue which has a show scheduled in future with X bookings. the venue capacity cannot be less than X.

### Summary

    Admin can view basic high level summary data in summary page
    If user need to view summary regarding particular show or venue in filtered date, he can navigate to advanced page and can use filter option to view it

#### Min Max constraints

    Show name can be size from 1 to 64
    Duration of show can be from 30 min to 200 mins
    Fare for show should be 50 to 300

    Venue name can be size from 1 to 32
    Venue location can be size from 1 to 32
    Venue Place can be size from 1 to 32
    Venue Capcity should between 10 to 300

    AdminCode should be of size 10

    First name can be size from 1 to 32
    Last name can be size from 1 to 32
    Phonenumber can be size  10
    EmailId can be size from 3 to 32
    UserName can be size from 3 to 32
    Password can be size from 8 to 32
