# Work Projects
## Website
I currently work at PROVE, developing a complex internal website for the company using Ruby and Javascript.

### Tech Stack
- **Backend**: Ruby on Rails, [Bullet Train](https://github.com/bullet-train-co/bullet_train)
- **Frontend**: Hotwire (Turbo & Stimulus), Tailwind CSS, JavaScript
- **APIs**: Google Maps API, MYOB API
- **Deployment**: AWS EC2, Nginx, Puma

### Features
Below is a brief summary of its features:
1. It stores quotes and jobs, and allows quotes to be awarded and converted to jobs, or reports to be made on the current productivity of a job or quote (or several jobs or quotes). These are attached to clients
1. It allows users to make timesheets, recording the hours they put into each job
1. Timesheets are used to pay the employees according to the current award for electricians. The website automatically determines and takes into account the travel time (based on a Google Maps API), the employees' hourly rates, any allowances they are entitled to, whether they travelled to or from home, the time they have been apprentices, overtime and double overtime, and many other factors
1. Timesheets are also used to invoice clients. These invoices use the hours employees have worked on a job, their hourly rates, their travel times, any expenditures, the price of subcontractors, and other factors
1. Employees can apply for and be granted leave. They can also submit medical certificates
1. Employees can read and acknowledge safe operating procedures
1. There are various roles, each granting different permissions. Permissions can given either to individual users or to groups, which users can then be assigned to. Both groups and individual users can be 

A staging version of this website can be explored at https://infra.proveng.com.au/. Log in with the following credentials:
    
    Email: mark@test.com
    Password: password

You can then explore the website. Note that all job and employee names (besides my own) are fake and were created by a spoofer. Also note that, because this account's credentials are publicly available, I have limited its permissions.

## App
For a specific job, I also developed a data entry app with the basic CRUD functions, as well as image uploading and data exporting functionalities. If you have an Android phone, you can try it by downloading the universal.apk file. Below is its tech stack:
- **Framework**: React Native (with Expo) 
- **Language**: TypeScript
- **Storage**: AsyncStorage