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
    Allocation are taken care like there should be 15 min break between end of one show and beggining of nect show

Todo Admin
Update Shoe duration and verify conlicts and throw error message
Create mqatplot graps
