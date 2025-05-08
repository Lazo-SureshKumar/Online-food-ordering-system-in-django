# Online-food-ordering-system-in-django
Food ordering System project in Python Django focuses mainly on dealing with managing food orders.

## Customer Panel:
In an overview of this web application, a user can simply register and start
using it.Here, the system displays all the available food items where the user can add them to the cart.
The user has to select amongst the available food choices.After all, the user can check cart,remove unwanted orders too.
And finally the user can place order.After place order,the user can view all food orders or cancel order.
when cancel the order if you pay through online it will return to your account after.

![Screenshot (64)](https://github.com/user-attachments/assets/f46dcb32-1215-488b-8952-2b4bb44020b0)


## Admin Panel:
On the other hand,the user can access the Django Administrator panel by providing admin credentials.
The Django adminstrator panel contains all the management sides of the system.It includes management of 
food menu,user,and orders.The admin can simply add more food items by providing details such as name,descrption,price,
and image to it.And admin simply change status as a delivered.

![Screenshot (65)](https://github.com/user-attachments/assets/12b5eafe-f7a8-4236-9179-f9f0e3b4a038)

### Features:
    Customer Panel
       - Add to Cart
       - Place Order
       - List Orders
    Admin Panel
       - Manage Food Items 
       - Manage Food Orders
       - Customer Management

### How To Run This Project
    Install Python()(Do not forget to Tick Add to Path while installing Pyhton)
    Open Terminal and Execute Following Commands:

    pip indtall django==3.0.5
    pip install django-bootstrap-v5 

    Download this Project Zip Folder and Extract it
    Move to project folder in Termial.Then run following Commands:

        python manage.py makemigrations
        python manage.py migrate
        python manage.py runserver

    To create superuser(admin):python
        manage.py createsuperuser

    Now enter following URL in Your Browser Installed On Your Pc
      http://127.0.0.1:8000/

    Drawbacks
        When user edit their profile then must login again because their username/password is updated in d.
  
