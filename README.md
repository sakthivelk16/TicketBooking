# TicketBooking

## User View

### Search

    User can search using 5 different parameter as follows
    - Search by Venue Name
    - Search by Venue Location
    - Search by Show Name
    - Search by Show Tags
    - Search by Show Ratings`

### Rating

    A user can can Rate a show on scale 1 to 5.
    A user can rate a show only once despite the number of booking on same shows in different venues

## Admin View

    Admin can create or edit or delete Show, Venue and allocation details
    venues and shows cannot be deleted unless their allocation is deleted

### Allocation constaraints

    Admins cannot edit details of allocation which is in the past
    Admin can create allocation after 15 mins from current time
    Allocation are taken care like there should be 15 min break between end of one show and beggining of next show


### Show Constraints
    We cannot create two show under same name

### Venue Constraints
    There can not be two venue name with same location
    There can be same venue name if location are different

#### common rules
    This application is case sensitive. please use captilized first letter and all letter in small for better usage

#### Rules
    Show name can be size from 1 to 64
    Duration of show ca be from 30 min to 200 mins
    Fare for show should be 50 to 300

    Venue name can be size from 1 to 32
    Venue location can be size from 1 to 32
    Venue Place can be size from 1 to 32
    Venue Capcity should between 10 to 300

    User can book any number of ticket subject to availability
    AdminCode should be of size 10
    
    first name can be size from 1 to 32
    last name can be size from 1 to 32
    Phonenumber can be size from 1 to 10
    EmailId can be size from 3 to 32
    UserName can be size from 3 to 32
    Password can be size from 8 to 32
