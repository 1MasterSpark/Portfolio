I currently work at PROVE, developing a complex internal website for the company using Ruby and Javascript. Below is a brief summary of its features:
1. It stores quotes and jobs, and allows quotes to be awarded and converted to jobs, or reports to be made on the current productivity of a job or quote (or several jobs or quotes). These are attached to clients
2. It allows users to make timesheets, recording the hours they put into each job
3. Timesheets are used to pay the employees according to the current award for electricians. The website automatically determines and takes into account the travel time (based on a Google Maps API), the employees' hourly rates, any allowances they are entitled to, whether they travelled to or from home, the time they have been apprentices, overtime and double overtime, and many other factors
4. Timesheets are also used to invoice clients. These invoices use the hours employees have worked on a job, their hourly rates, their travel times, any expenditures, the price of subcontractors, and other factors
5. Employees can apply for and be granted leave. They can also submit medical certificates
6. Employees can read and acknowledge safe operating procedures
7. There are six different roles, each granting different permissions. I am currently overhauling this system in favour of an improved one

A staging version of this website can be tested at https://infra.proveng.com.au/. Opening this URL will show a screen saying that the website is insecure (since it is just for testing, so I did not set up a certificate as I did on the main site). Press "Advanced" then proceed anyway. Log in with the following credentials:
    
    Email: mark@test.com
    Password: password

You can then explore the website. Note that all job and employee names (besides my own) are fake and were created by a spoofer.
