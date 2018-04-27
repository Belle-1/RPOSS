# Software Requiremsnts Specification
## Restaurant POS System (RPOSS)

## Table Of Contents
1. [Intorduction](#introduction)
   - [Purpose](#purpose)
   - [Scope](#scope)
   - [Definitions, acronyms, and abbreviation](#definitions-acronyms-and-abbreviation)
   - [References](#references)
   - [Overview](#overview)
2. [Overall Description](#overall-description)
   - [Product Perspective](#product-perspective)
   - [Product Functions](#product-functions)
   - [User Characteristics](#user-characteristics)
   - [Operating Environment](#operating-environment)
   - [Constraints](#constraints)
   - [Assumptions and Dependencies](#assumptions-and-dependencies)
3. [External Interface Requirements](#external-interface-requirements)
   - [User Interface](#user-interface)
     - [Restaurant Customers](#restaurant-customers)
     - [Restaurant Staff](#restaurant-staff)
     - [Restaurant Owner](#restaurant-owner)
   - [Hardware Interfaces](#hardware-interfaces)
   - [Software Interfaces](#software-interfaces)
   - [Communication Interfaces](#communication-interfaces)
4. [System Features](#system-features)
   - [Restaurant Customers](#restaurant-customers)
     - [Restaraurant Built-in Home Page](#restaraurant-built-in-home-page)
       - [Navigation Bar](#navigation-bar)
       - [Welcom Section](#welcom-section)
       - [About Us Section](#about-us-section)
       - [Menu Section](#menu-section)
       - [Our Location Section](#our-location-section)
       - [Contact Us Section](#contact-us-section)
     - [Menu Built-in Page](#menu-built-in-page)
       - [Menu Items Section](#menu-items-section)
       - [Checkout Section 1](#checkout-section-1)
     - [Form Built-in Page](#form-built-in-page)
       - [Form Section](#form-section)
       - [Checkout Section 2](#checkout-section-2)
     - [Verifying Phone Number](#verifying-phone-number)
     - [We Received Your Order Built-in Page](#we-received-your-order-built-in-page)
   - [Restaurant Staff](#restaurant-staff)
     - [Progressive Panel](#progressive-panel)
       - [Navigation Bar](#navigation-bar)
       - [Hello Section](#hello-section)
       - [Menu Bar](#menu-bar)
         - [All Orders View](#all-orders-view)
         - [Pending Orders View](#pending-orders-view)
         - [In Progress Orders View](#in-progress-orders-view)
         - [Finished Orders View](#finished-orders-view)
         - [Missed Orders View](#missed-orders-view)
   - [Restaurant Owner](#restaurant-owner)
     - [Owner Panel](#owner-panel)
       - [Navigation Bar](#navigation-bar)
       - [Hello Section](#hello-section)
       - [Menu Bar](#menu-bar)
         - [Restaurant Option](#restaurant-option)
           - [Base Information](#base-information)
           - [Openning Hours](#openning-hours)
           - [Social Media](#social-media)
         - [Menu Options](#menu-options)
           - [Menu Setup](#menu-setup)
         - [Order Hampers](#order-hampers)
           - [Ordering Methods](#ordering-methods)
           - [Orders Timing](#orders-timing)
         - [Employees Registration](#employees-registration)
           - [Add a New Employee](#add-a-new-employee)
         - [System Interfaces](#system-interfaces)
           - [Online Ordering](#online-ordering)
5. [Other Nonfunctional Requirements](#other-nonfunctional-requirements)
  - [Performance Requirements](#performance-requirements)
  - [Safety Requirements](#safety-requirements)
  - [Software Quality Attributes](#software-quality-attributes)
6. [Other Requirements](#other-requirements)
  - [Twilio](#twilio)
  - [SMTPlib](#smtplib)
7. [Release Plan](#release-plan)
     
## Intorduction
### Purpose
The purpose of this documentation is to give a detailed description of the requirements and features for the "Restaurant POS System" (RPOSS) .it will illustrate the purpose and complete declaration for the development of the system. it will also explain system constraints, interfaces and interaction with other external devices/systems. this document is primarly intended to be a reference for developing the first version of the system for the development team.

This document is going to serve as the stepping stone for the upcoming versions of this system.
### Scope
The Restaurant POS System (RPOSS) is an application designed for restaurants' owners, not only to imrpove the customer's experience, but also to ease the workload on the restaurant staff by providing the online-ordering functionalities to the restaurant website.
 	 
The RPOSS application is hosted on a cloud hosting service which means the system does not need any infrastructure downloaded on the restaurant premises. For all different users of the system need to be able to use it is a web browser, meaning this application works on any device.
### Definitions, acronyms, and abbreviation
| Term | Definition |
| --- | --- |
| POS | Point Of Sale. |
| Restaurant Owner | someone who owns a local restaurant and wants his restaurant to be extended by the RPOSS. |
| Restaurant Staff | Restaurant staff members(aka employees, workers). |
| RPOSS | The name of this application. stands for: Restaurant Point Of Sale System. generally reffered to as a system or an application. |
| restaurant website | overall restaurant web application which holds: restaurant built-in web pages, owner web panel, and progressive panel. |
| restaurant home page | Restaurant built-in home page which the customers will see and interact with. |
| owner panel | It is a web page only the restaurant owner can access to add and/or change restaurant informations and options. |
| progressive panel | It is a web page only the restaurant owner can access to add and/or change restaurant informations and options. |
| web browser | Any web browser running on any device. |
| thermal printer | A printer that uses heated pins to burn images onto heat-sensitive paper. |
| DESC | Description |
| RAT | Rational |
| DEP | Dependency |
### References
- [IEEE Software Engineering Standards Committee, "IEEE Std 830-1998, IEEE Recommended Practice for Software Requirements Specifications", Octoper 20. 1998.](https://goo.gl/nsUFwy)
- [Software RequirementsSpecification-Amazing Lunch Indicator](http://www.cse.chalmers.se/~feldt/courses/reqeng/examples/srs_example_2010_group2.pdf)
## Overall Description
This section will give an overview of the whole system. The system will be explained in its context to show what the different parts of this applicaiton are and how do these parts interact with each another and how do they interact with some external devices. 
this section will also provide the basic functionality of this application.
it will also describe what type of stakholders that will use the application and what functionality is available for each type.
at last, the constraints and assumptions for the application will be presented.
### Product Perspective
The RPOSS project is a self contained product which runs on any web browser for all the different users of the application. while the restaurant web application is the main focus of the system, there is also a server-side component and an API integeration that will be responsible for adding and modifying on the database and responsible for SMS verification services. A thermal printer hardware is also attached to the system for printing receipts for the customers.

![alt text](https://github.com/Belle-1/RPOSS/blob/master/diagrams/Component%20Diagram%20-%201.png)

the restaurant web application is further divided into three panels: owner panel which will allow him/her to define basic information and different options about the restaurant. the second panel is the staff progressive panel, this panel is responsible for showing the customers orders, it gives the staff members the ability to accept and reject pending orders.the third panel is the Restaurant built-in home page, basically, this is the main web page for the restaurant which shows up to customers. it will hold the information architecture of the restaurant that the owner specified in his/her panel, plus the online ordering functionality. 
Unlike the restaurant customers, both the restaurant owner and staff need special credaentials in order for them to be able to access their web panels.

This system is designed with a built-in restaurant web pages, In case the restaurant owner has his/her website and all they need is the online ordering functionality that RPOSS provides, The system can provide them with an "order online" button which they can add to their website. This button will lead the customer directly to the built-in restaurant menu page where restaurant customers get to check menu items for pick-up and delivery orders.

Since this is a data-centric product it needs somewhere to store data. for that, a database will be used. all of the web application parts will communicate with the database, however in slightly different ways. restaurant home page and its sub-pages will add data to the database, while owner web panel and staff progressive web panel will use the database for creating, reading, updating and deleting data. all of the database communication will go over the internet.

This system will be involved with the Twilio API, which will be used for its SMS two-factor(2FA) authentication services for confirming customers' identities.

### Product Functions
The following table offers a brief outline of the main features and functionalities of the RPOSS. The features are split into three major user classes: Restaurant owner, Restaurant staff and restaurant customers.

| User | Features |
| --- | --- |
| **Owner** | Restaurant base information |
|  | Restaurant menu |
|  | Ordering hampers |
|  | Opening hours |
|  | Employee registration |
|  | System interfaces |
| **Staff** | View orders |
|  | Confirm orders |
|  | Reject orders |
|  | Fininshing orders |
|  | Printing receipts |
| **Customers** | Checkout menu items |
|  | Restaurant built-in home page |
|  | phone validation |
|  | E-mail notification messages |
|  | Placing delivery orders |
|  | Placing pick-up orders |
### User Characteristics
The application is intended for use by three user classes: restaurant customers, restaurant owner and restaurant staff. Each of these three types of users has different use of the system so each of them has their own requirements.

1. **Restaurant owner**, who wants his/her restaurant to be part of the RPOSS. through his/her web panel. there they will manage basic information and different options about their restaurant, for example a description of the restaurant, contact information and their menu.

2. **Restaurant staff**, they will interact with the progressive web panel. there they will get to manage all  placed orders by customers.

3. **Restaurant customer**, could be any kind of person who wants to order some food online and get delivered. customers will interact mainly with the restaurant built-in home page and the menu built-in page.

### Operating Environment
The restaurant application will run on any web browser on any device accessing the internet.

The web application of this system is highly interacted with the RPOSS server, a vertual dedicated server hosted by DigitalOcean.com. The server operates on a Windows <version> platform with 1GB of RAM and 25GB of allocated storage space(those values can be resized up or down at any time). The RPOSS database will be stored on the server using MySQL and will be interfaced with the SQL-Alchemy Flask extension.
### Constraints
The RPOSS is developed in Python, it uses Python ESC/POS library for accessing thermal printers that are handled by ESC/POS commands. So the system is constrained by the type of the thermal printer linked to it. since there are multiple printer vendors and drivers, the system will most likely not be able to recognize all different types of them.

the internet connection is also a constraint for two reasons: one, the entire web-portal with its different panels, can only be accessed through internet using a web browser. two, this application sends and fetches data from the database over the internet, it is crucial that there is an internet connection for the application to function.
### Assumptions and Dependencies
One assumption about the product is that it will always be accessed through a web browser, an internet connection is a must in order for all users of the system to connect to the web application and the database. for example, the restaurant staff can not access the progressive panel and change orders status if there is no internet connection.

Another assumption is that the thermal printer connected to the system is compatible with the ESC/POS command set. if it has different command set, the system needs to be specifically adjust to the currently existing printer type.

Another assumbtion is that the restaurant has one branch only. this version of the system does not support multiple branches.

This system is highly depedent on the Twilio API service. a Twilio account must be created manually for the restaurant in order for the web application to be able to validate customers' identities.

This system also depends on the Python SMTPlip for sending email messages from the server to the restaurant customers.
## External Interface Requirements
### 1. User Interface
As mentioned before, there are three types of users that interact with the system: restaurant customers, restaurant owner and restaurant staff. Each of them has their own interface to the system.
#### 1.1. Restaurant Customers
a customer will first see the restaurant home page. the restaurant home page holds most of the informations that the owner defined in his/her panel. those informations will help the customer to know more about the restaurant. for example, menu description, contact information, restaurant location, etc.

In the restaurant built-in home page, there must be a button that leads to the restaurant built-in menu page. customers will get to place orders there by adding menu items for checkout.

After choosing menu items, the customer has to fill in a generic form, this form includes: full name, phone number, E-mail address, whether the order is a Pick-up or Delivery. If the order method is Delivery, customer must provide his/her address location.

Next, customers will be asked to verify their phone number with the code the system sent them to complete placing the order.

when phone number is verified, then, within a period of 5 minutes, a confirmation email message is sent to the customer to aknowledge them that the order is confirmed. if the order was rejected or was not confirmed within a period of 5 minutes by the restaurant staff, a rejection message will be sent to the customer email. the confirmation email message will state: order id, order details, customer's details, and when will the order be ready.

[see Figure](https://github.com/Belle-1/RPOSS/blob/master/prototypes/customer.pdf)
#### 1.2. Restaurant Staff
The restaurant staff interact with the system through the Progressive Panel web page. Before that, a restaurant employee must log in to the system using credentials that the owner provide them in the www.restaurantname.com/RPOSS/login.

The progressive panel web page holds five different views of the orders:
-**Pending orders view**: this view will show all orders made by customers waiting for an approval of the restaurant staff.
-**In Progress orders view**: this view will hold accepted orders. this view is especially designed for the restaurant cooks, so that it will show each orders menu items and their expected preparing time clearly. pressing the finished button on an order aknowledges that the order is done.
-**Finished orders view**: will show all orders that are finished/delivered successfully.
-**Missed orders view**: this view will hold all rejected/missed orders.
-**All orders view**: in this view, the staff will get to see al orders from pending to missed. this view is sorted by time.

Finally, the restaurant employee can exit the system using the log out link in the progressive panel page.
[see Figure](https://github.com/Belle-1/RPOSS/blob/master/prototypes/staff.pdf)
#### 1.3. Restaurant Owner
Same as restaurant staff, the restaurant owner will go through the log in page to get into the system using a predefined credentials.

Once the owner is logged in to the system they can get access to the following options:
-**Restaurant Information** / The owner can add basic information about the restaurant, opennig hours and social media accounts.
-**Restaurant Menu** / This section is where the owner will add his/her menu items.
-**Ordering Hampers** / This section gives the owner the ability to control what kind of ordering methods does the restaurant offer to the customers. This section also asks for estimations on times by which a specific order will be done. 
-**Employees Registration** / The owner is responsible for making the employees accountsin which they will use to access the RPOSS.
-**System Interfaces** / In case the owner has his/her own website and all they are intrested in is the online ordering functionalities. They can get to this section and take the online ordering button and link it to their website.
[see Figure](https://github.com/Belle-1/RPOSS/blob/master/prototypes/owner.pdf)
### 2.Hardware Interfaces

The RPOSS web application can and will run on any device with a web browser installed on it.

For all Users to be able to access the restaurant website, an internet connection is needed. So a network device such as a modem is required.

The approached thermal printer must support the ESC/POS command set. Restaurant owner and staff must take into consideration that the approached printer must be compatible with the device used to get to the restaurant website. for example: some printers can run over bluetooth others do not, some can be attached to a specific operating systems and others don't.
### 3.Software Interfaces
The RPOSS depends on some libraries for its functions. These tools are already pre-included with the application.

| Service/Software name | Functionality of the software | accomplishes this system requirements |
| --- | --- | --- |
| Twillio | - Two-Factor(2FA) authentication service. - Alphanumeric sender ID. | - Verifying restaurant customers' identities. - Sending SMS messages using a personalized sender name. |
| jQuery-AJAx | Request JSON from remote server. | Requesting and receiving data from server. |
| SMTPlib | Sending e-mails. | Sending confirmation e-mails to customers. |
| Network device | Provides internet access. | Connect restaurant users to the RPOSS. |

In addition to that, an email service application such as outlook.com, gmail.com, etc. is required in order for the restaurant staff menmbers to communicate with the customers messages being sent from the contact use built-in section.
### 4.Communication Interfaces
The communication between the different parts of the system is important since they depend on each another. Some of these communications are habdled by the underelying operations systems, others have to be set manually by the developer along with the restaurant owner.

| Service/Software name | Functionality of the software | accomplishes this system requirements |
| --- | --- | --- |
| ECS/POS | Accessing printers handled by ESC/POS commands from python application. | Attaching thermal printer to the application |
| Bootstrap | Designing web applications. | For the restaurant to be visually apealing & easily navigated.  |

## System Features
In this section, RPOSS features and functions will be listed and described for better understanding and to help developers with the implementation process.
### 1. Restaurant Customers
#### 1.1. Restaraurant Built-in Home Page

| ID | FR1 |
| --- | :--- |
| TITLE | Restaurant built-in home page |
| DESC | This pre-defined page will hold most of the information defined in the owner panel, This page include the following sections: Navigation bar, Restaurnat welcom section, About section, Menu section, Location section, Contact section. |
| RAT | In order for the restaurant customer to interact with the application. |
| DEP | FR24, FR25, FR26, FR27, FR31 |
##### 1.1.1. Navigation Bar

| ID | FR2 |
| --- | :--- |
| TITLE | Navigation bar |
| DESC | This navigation bar will hold the following: Restaurnat logo, Restaurant name, link to the About section, link to the Mneu section, Link to the Contact sesction, Link to the Location section. |
| RAT | In order for the customers to navigate the restaurant built-in website easily. |
| DEP | FR1, FR24, FR26, FR8 |
##### 1.1.2. Welcom Section

| ID | FR3 |
| --- | :--- |
| TITLE | Welcom section |
| DESC | This section is the first part of the Restaurant built-in home page that the customer will see. It will show the restaurant name, restaurant welcom section image, a welcoming phrase and the order online button. |
| RAT | None. |
| DEP | FR1, FR24, FR31 |
##### 1.1.3. About Us Section

| ID | FR4 |
| --- | :--- |
| TITLE | About us section |
| DESC | This section will hold the restaurant about description and opening hours that the owner specified in his/her panel. |
| RAT | In order for the customers to have a general idea about the restaurant. and its working days/times. |
| DEP | FR1, FR24, FR25 |
##### 1.1.4. Menu Section

| ID | FR5 |
| --- | :--- |
| TITLE | Menu section |
| DESC | This sectio will hold the restauran menu description, image, and the online ordering button. |
| RAT | In order to provide the cuctomers a way to the menu built-in page and tp provide them with a general idea about the restaurant menu. |
| DEP | FR1, FR27, FR31 |
##### 1.1.5. Our Location Section

| ID | FR6 |
| --- | :--- |
| TITLE | Our location section |
| DESC | This sectio will hold the following: Restaurant address line, Restaurant opening hours, Restaurant city, counttry, ZIP code, Restaurant phone code, Restaurant email address, Restaurant social media account. |
| RAT | In order for the customer to have informations about the restaurant location. |
| DEP | FR1, FR24, FR25, FR26 |
##### 1.1.6. Contact Us Section

| ID | FR7 |
| --- | :--- |
| TITLE | Contact us section |
| DESC | This sectio will hold a field that the customer can submit to the restaurant email address, a customer must provide the following: Full name, Email address, Phone number, message. |
| RAT | In order for the customer to contact the restaurant. |
| DEP | FR1 |
#### 1.2. Menu Built-in Page
##### 1.2.1. Menu Items Section

| ID | FR8 |
| --- | :--- |
| TITLE | Menu items section |
| DESC | This section of the menu page will show all the restaurant menu items. Items will be categorized by their Category. Each item will show its name, price, and image. |
| RAT | In order for customers to see and choose from the menu. |
| DEP | FR27 |
##### 1.2.2. Checkout Section 1

| ID | FR9 |
| --- | :--- |
| TITLE | Checkout section 1 |
| DESC | This section will hold all items that the customer chose from the menu items section. Each item will show its name. image, price, quantity, total price(item price * its quantity). A customer can delete an item and remover/add to an item quantity from the checkout section. A customer can also clear all items placed in the checkout section. This section will show the subtotal, tax, delivery charges, total amount of the order. If the checkout section holds no item, the customer can not proceed with the order. |
| RAT | In order for customers to checkout menu items. |
| DEP | RF8, FR28 |
#### 1.3. Form Built-in Page
##### 1.3.1. Form Section

| ID | FR10 |
| --- | :--- |
| TITLE | Form section |
| DESC | This section will hold the field that the customers has to fill in order to send their orders. These fields are: full name, phone number, email address, order method(pick-up, delivery), and special instruction field for the customer's notes. In case the customer shoose delivery as an order method, the customer must provide his/her address line 1, address line 2, state, zip code. |
| RAT | In order for customers to provide their personal informations. |
| DEP | FR9, FR28 |
##### 1.3.2. Checkout Section 2

| ID | FR11 |
| --- | :--- |
| TITLE | Checkout section 2 |
| DESC | this section will hold the same informations as the checkout section 1 except that it is for reviewing purposes which means customers can not change its values. |
| RAT | In order for a customer to review his/her order's details. |
| DEP | FR9 |
#### 1.4. Verifying Phone Number

| ID | FR12 |
| --- | :--- |
| TITLE | Verifying phone number |
| DESC | Given that the system has sent SMS verifying message containing X digits code to the customer's phone number, The customer is asked to type in that code in this page. This page will also provide the customer with a way of resending the code and a way of cancelign the order. |
| RAT | In order for the system to verify the customer identity. |
| DEP | None. |
#### 1.5. We Received Your Order

| ID | FR13 |
| --- | :--- |
| TITLE | We received your order page |
| DESC | Given a customer has verified his/her phone number, only then they will get access to this page. This page will aknowledge the customer with the time an order need before it takes a confirmation form the restaurant staff. This page will contain the customer's order details and the customer's personal details. This page will provide a way of going back to the Restaurant website. |
| RAT | In order for the customer to have a feedback about his/her order. |
| DEP | FR12, FR10, FR11, FR29 |
### 2. Restaurant Staff
#### 2.1. Log In Page

| ID | FR14 |
| --- | :--- |
| TITLE | Log in page |
| DESC | **Senario**: restaurant staff member: Given that the restaurant staff member has been given credentials by the restaurant owner in order for him/her to get into the RPOSS. A restaurant staff member must provide a name and a password.|
|  | **Senario**: restaurant owner: Given that the restaurant owner is given a pre-defined credentials to access the RPOSS. the restaurant owner must provide these credentials in order for him/her to access the RPOSS. |
| RAT | In order for restaurant owner and staff members to get into the RPOSS. |
| DEP | FR30 |
#### 2.2. Progressive Panel
##### 2.2.1. Navigation Bar

| ID | FR15 |
| --- | :--- |
| TITLE | Navigation bar |
| DESC | This navigation bar will hold the restaurant logo, restaurant name, and a log out option. |
| RAT | In order for the restaurant staff to log out of the restaurant. |
| DEP | FR24 |
##### 2.2.2. Hello Section

| ID | FR16 |
| --- | :--- |
| TITLE | Hello section |
| DESC | This section will show the employee's name. |
| RAT | In order for the system to differentiate employees. |
| DEP | FR14 |
##### 2.2.3. Menu Bar
2.2.3.1. All Orders View

| ID | FR17 |
| --- | :--- |
| TITLE | All orders view |
| DESC | This section will show all orders the system has/had in a table view. This table contains: Order ID, Confirmed/rejected by, Customer's name, Custoemr's phone number, Time made, Order method(delivery/pick-up), Status(pending, in progress,deliverd, rejected), Time confirmed/rejected. |
| RAT | In order to view all orders. |
| DEP | FR18, FR19, FR20, FR21 |

2.2.3.2. Pending Orders View

| ID | FR18 |
| --- | :--- |
| TITLE | Pending orders view |
| DESC | -This view will show all pending orders that the system currently has.|
|  |-Each order will view: order method, order ID, customer's name, total amount, status(pending), pending remaining time.|
|  |-once clicked, a pending order will show additional information beside the aforementioned informations: customer's personal details, customer's order details, special instructions, confirm and reject buttons.|
|  |-The customers must receive an email telling them whether the order was confirmed or rejected.|
|  |-a receipt will be printed once an order is confirmed. |
| RAT | In order for restaurant staff to confirm or reject placed orders. |
| DEP | FR13 |

2.2.3.3. In Progress Orders View

| ID | FR19 |
| --- | :--- |
| TITLE | In progress orders view |
| DESC | -This view will show all confirmed orders that are in progress now.|
|  |-Each order will show: order ID, preparing remaining time, order's menu items, and a finish button.|
|  |-This view is for replacing using receipts for tracking orders by the restaurant's cooks.|
|  |-Once clicked, the order will change color to notify restaurant staff that this order is being worked on.|
|  |-Once preparing time is finished, automatically, the order will considered finished. |
| RAT | In order for progressing the customer's order. |
| DEP | FR18, FR13 |

2.2.3.4. Finished Orders View

| ID | FR20 |
| --- | :--- |
| TITLE | Finished orders view |
| DESC | This view will show all finished orders in a table view, This table contain: order ID, confirmed by, customer's name, custoemr's phone number, time made, order method(delivery/pick-up), status(deliverd), time confirmed. |
| RAT | In order to view all finished orders. |
| DEP | FR19 |

2.2.3.5. Missed Orders View

| ID | FR21 |
| --- | :--- |
| TITLE | Missed orders view |
| DESC | This view will show all missed/rejected orders in a table view, This table contain: order ID, rejected by, customer's name, custoemr's phone number, time made, order method(delivery/pick-up), status(missed/rejected). |
| RAT | In order to show all missed/rejected orders. |
| DEP | FR18 |
#### 3. Restaurant Owner
##### 3.1. Owner Panel
###### 3.1.1. Navigation Bar

| ID | FR22 |
| --- | :--- |
| TITLE | Navigation bar |
| DESC | It will hold: restaurant logo, restaurant name, log out. |
| RAT | In order for the owner to log out of the system. |
| DEP | FR24 |
###### 3.1.2. Hello Section

| ID | FR23 |
| --- | :--- |
| TITLE | Hello section |
| DESC | This section will show the owner name as specified in the pre-defined credentials. |
| RAT | In order to differentiate the owner when logged to the system. |
| DEP | FR14 |
###### 3.1.3. Menu Bar
3.1.3.1. Restaurant Option

   3.1.3.1.1. Base Information
   
| ID | FR24 |
| --- | :--- |
| TITLE | Base information |
| DESC |  In this section the owner will provide basic information about his/her restaurant, those informations include: restaurant name, restaurant about, restaurant built-in welcom section image, restaurant address line, restaurant city, restaurant country, restaurant ZIP code, restaurant email address, restaurant phone number, and restaurant logo. |
| RAT | In order for the owner to provide his/her restaurant basic informations. |
| DEP | FR1 |

   3.1.3.1.2. Openning Hours
      
| ID | FR25 |
| --- | :--- |
| TITLE | Opening hours |
| DESC | In this section the owner will provide the restaurant openning hours and working days. |
| RAT | In order for the owner to specify opening hours/working days. |
| DEP | FR4, FR6 |

   3.1.3.1.3. Social Media
      
| ID | FR26 |
| --- | :--- |
| TITLE | Social media |
| DESC | In this section the restaurant can provide the restaurant's social media accounts for the following websites: Facebook, Twitter, Instagram, Snapchat, Yelp. |
| RAT | In order for the owner to provide the restaurant's social media accounts. |
| DEP | FR6 |

3.1.3.2. Menu Options

   3.1.3.2.1. Menu Setup
      
| ID | FR27 |
| --- | :--- |
| TITLE | Menu setup |
| DESC | -In this form the restaurant owner will get to provide the following: an image for the menu built-in section and a description for the built-in menu section.|
|  |-The owner also get to add to the menu items table, this table will contain the follwoing: item ID, item name, item category, item status(active, inactive, delete), item price, item size, item desc, item image.|
|  |-Once an item is added to the menu items table, the owner can delete it, change its state, change its size. |
| RAT | In order for the owner to add items to the restaurant menu. |
| DEP | FR5 |

3.1.3.3. Order Hampers

   3.1.3.3.1. Ordering Methods
    
| ID | FR28 |
| --- | :--- |
| TITLE | Ordering methods |
| DESC | -Pick-up: The owner get to choose whether they allow pick-up orders or not, they also can specify a tax value for pick-up orders.|
|  |-Delivery: The owner get to choose whether they allow delivery orders or not, owners also can specify taxes, delivery charges, minimum order amount, and maximum order amount.|
|  |-The only payment method that the system support in this version is Cash On Delivery(COD). |
| RAT | In order for the owner to specify ordering options that they want in their restaurant. |
| DEP | RF9, FR10, FR11 |

   3.1.3.3.2. Orders Timing
    
| ID | FR29 |
| --- | :--- |
| TITLE | Orders timing |
| DESC | In this section the owner will get to specify the delivery time, preparing time, and pending time for which each order will take.|
|  |-Delivery time: time between placing an order and receving it.|
|  |-Preparing time: time by which the order is ready to be delivered(for pick-up orders).|
|  |-Pending time: time by which the order has to be confirmed by the restaurant staff. if the order was not confirmed within the specified time, the order is considered missed. |
| RAT | In order for the restaurant owner to specify orders timing. |
| DEP | FR18, FR19 |

3.1.3.4. Employees Registration

   3.1.3.4.1. Add a New Employee
       
| ID | FR30 |
| --- | :--- |
| TITLE | Add a new employee |
| DESC | In this form the owner can add an employee account to the system by providing an employee name, employee email, and employee password. All employees account will show in the employees table as follows: employee ID, employee name, status(active, inactive, delete), and employee email. |
| RAT | In order for the restaurant owner to add employees to the system. |
| DEP | FR14  |

3.1.3.5. System Interfaces

   3.1.3.5.1. Online Ordering
       
| ID | FR31 |
| --- | :--- |
| TITLE | Online ordering |
| DESC | This section will provide the restaurant owner with the code of the online ordering button so he/she can add it to his/her website. |
| RAT | In order for the owner to add online ordering functionality to his/her website. |
| DEP | FR8, FR27 |
## Other Nonfunctional Requirements
### 1. Performance Requirements
The RPOSS is not a resi=ource consumer and will run on almost every device with a web browser installed on it. its functions and features  are not computationally intensive. The only real requirements are: web browser, thermal printer and an internet connection.
### 2. Safety Requirements
To eliminate data loss posibility, the remote is backed-up by the DigitalOcean cloud service.
### 3. Software Quality Attributes
The application provides a quite friendly user interface with its operations accessible from the application's different web panels. an average or casual user should not define any problem using the application to perform its main functions.
## Other Requirements
### 1. Twilio
The system has to sign an upgraded twilio account in order to use the following:
-Two-factor(2FA) authentication services: for verifying customers' identities.
-Alphanumeric ID: for sending SMS messages using a personalized sender name.
### 2. SMTPlib   
For the system to be able to send and receive confirmation messages to the customers, there must be an email assigned for accomplishing these requirements.

## Release Plan
since this app is mostly RESTfull API architectural styled, here is the implementation plan that i followed:
- [x] Mock-ups.
- [x] Routing.
- [x] Templates & forms.
- [x] CRUD functionalities.
- [ ] API endpoints.
- [ ] Styling and message flashing



