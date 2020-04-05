Project Name |
------------ |
Secure Purchase Order

Group Members |
------------- |
Brian Lim
Mahendra Pruitt
Marc Suda
Narchel DaCosta

DISCLAIMER: In order to view this markdown file properly, you need to use a supported IDE such as Atom, Sublime Text 3 or Visual Studio or view it on GitHub.

---

## **Initial Setup**
###### Install Ubuntu 18 w/ Python 3.7 or above

###### Install the image onto a virtual box:
###### After installing, the machine was updated whenever prompted
![Ubuntu Installation](screenshots/image5.png)

---

## **Required Dependencies**
###### Before any work is done, the following dependencies are required for the project
###### Django
###### Django Crispy Forms
###### Python 2 / Python 3

To install Django, you need pip, so enter the following command:
`sudo apt-get install python3-pip`

from there, you can now install Django using the following command:
`python3 -m pip install django`

lastly, you need to install Django Crispy Forms using the following command:
`python3 -m pip install django-cripsy-forms`

NOTE: When we were developing the project, we had Django 3.0.4 and Python 3.6.9 Installed

---

## **Accessing The Site**
###### Be sure to have all the dependencies installed before moving forward!
###### To start the server and access the website, you need to first navigate to the `/spo-final/spo` directory via terminal and type the following command:
`python3 manage.py runserver`

From there, you can now open a new web browser and go to the following URL:
`127.0.0.1:8000`

If needed, you can also login via the Admin page by accessing the following URL: `127.0.0.1:8000/admin`

**Test Account Credentials**

Username | Password
-------- | --------
user | user
supervisor01 | supervisor01
purchase01 | purchase01
admin | admin

Once you're on the website itself, a regular user has access to create their own orders using the `New Order` button at the top bar

![new order](screenshots/image9.png)

> For security and privacy reasons, users are not able to view another user's order

![users order](screenshots/image12.png)

> As another added security precaution, users are not able to access another user's order by incrementing the order number in the address bar

For example, if you were to try and do that, you would be redirected to a `403 Forbidden error page`

![forbidden error](screenshots/image17.png)

> All Supervisor and purchasing department accounts will have full access to all user's posts

In order to have an account become a member of the supervisors or purchasing department, you need to do the following through the portal:
1. Log into the admin portal
2. Click on "users"
3. Click on the user in question
4. Check or uncheck "Supervisor status" or "Purchasing department status" located at the bottom of the page

![account update](screenshots/image13.png)
---
## **Account Privileges**

• Supervisors have the ability to `Approve` users posts when they click on the post

• Purchasing department users are able to purchase the item(s) using the `Purchase` button

• Someone who belongs to both departments will have access to both buttons

• Both departments will be allowed to verify and check the signature of the order by first clicking `Verify` and then clicking `Check Hash`

![verify](screenshots/image8.png)

• A user CANNOT update their purchase order once the order has been approved, a `403 Forbidden Message` will appear

---
## **Security | Encryption Information**

• Supervisor hash checking is only available to the purchasing department

• purchasing department hash checking is only available to the supervisor department

• If a supervisor hasn't approved, the purchasing department won't see a valid signature

• If a purchaser hasn't purchased, the supervisor won't see a valid signature

• In order to actually perform the signing and the verification, we use `4 libraries`

![libraries](screenshots/image10.png)

• Everything is done in the views.py file in the purchaseorder directory

---

## **Hashing Process**

When an order is approved or purchased, we use 2048-bit generated RSA private key for the respective department `(which are the .pem files)`

The hashing is done using SHA-256 and signed using the key. This is all performed once a supervisor or purchaser clicks the `Approve` or `Purchase` button:

![SHA-256 Hashing](screenshots/image21.png)

The verification is done in the orderVerify class within `purchaseorder/views.py`:

![verification](screenshots/image14.png)

Since the user can never change the order after it is updated, the signatures will always come back valid. Whether or not the order is approved, verified, etc is kept within a variable of the object. The full class can be viewed under `spo/purchaseorder/models.py`

![models](screenshots/image1.png)

Most of this functionality is provided by the purchaseorder module/directory. In terms of user authentication, that is provided by the users module/directory. While authentication is handled by Django, their user profile class had to be extended to accommodate our needs.

---

## **Setting Up From Scratch**

There may be the need to delete the pre-provided db.sqlite3 file so that you can setup the server from scratch. Setting up from scratch means that you won't have any users or admins.

To setup the server again, you should first delete the `.sqlite3` file:

Secondly, you should open up a new terminal window and `cd` into the directory of the `spo` folder containing the manage.py file.

In order to recreate the the database, tables and create a superuser (admin) account, the following commands must be done in order:

1. `python3 manage.py makemigrations`
2. `python3 manage.py migrate`
3. `python3 manage.py migrate --run-syncdb`

You should see the following output:

![recreate database](screenshots/image19.png)

Once completed, you can create a new admin account using the following command:

`python3 manage.py createsuperuser`

and enter an admin username and password. **This account will be able to access the admin portal**

Finally, run the following command like before to start the server:

`python3 manage.py runserver`

Then create any user you want by accessing the register page at: `127.0.0.1:8000/register`

**REMINDER**

**By default, an account is not a supervisor or member of the purchasing department or even the administrator. You will have to change those values via the admin portal.**
