# adgency-ai-assingment

# Project Readme

## Technologies Used
- Python 3.9.6
- Flask
- Bycrypt (for password hashing)
- Marshmallow (for validation)
- MongoDB (for data storage)
- AWS EC2 (to host MongoDB and this REST API service)

## Installation Guide

1. **Install Python Environment:**
   - Ensure that Python 3.9.6 is installed on your machine.

2. **Create Python Environment:**
   - Create a virtual environment using your preferred method (e.g., `virtualenv`).
     ```
     virtualenv venv
     ```

3. **Activate the Environment:**
   - Activate the virtual environment.
     - On Windows:
       ```
       .\venv\Scripts\activate
       ```
     - On Linux/macOS:
       ```
       source venv/bin/activate
       ```

4. **Install Requirements:**
   - Install the project dependencies using the provided `requirements.txt` file.
     ```
     pip install -r requirements.txt

## File Structure

- **blueprint**: Contains user and book module blueprints.
- **dto**: Contains user and book DTOs.
- **adgency-ai.postman collection**: Import this Postman collection to test the APIs.
- **app.py**: Creates Flask and database connections along with other required connections.
- **decorators.py**: Contains JWT authentication, admin authorization required decorators, and other required decorators.
- **constants.py**: Contains constants used throughout the project.
- **schema.py**: Contains all the serializers used for schema validation.
- **.env**: Contains environment variables for the project.

## API Endpoints

### 1. `book/search`
- **Method**: GET
- **Header**: Authorization
- **Query Params**: title, author, genre
- **Description**: Search for a book using the given parameters.

### 2. `book/filter`
- **Method**: GET
- **Header**: Authorization
- **Query Params**: rating, publication_year, genre
- **Description**: Filter books using the given parameters.

### 3. `book/ratings`
- **Method**: PUT
- **Header**: Authorization
- **Description**: Update all book ratings from the reviews and ratings submitted by users. Calculates the average rating and returns the value in the range of 1 to 10.

### 4. `book/create`
- **Method**: POST
- **Header**: Authorization
- **Request**: name, title, author, genre, publication_year
- **Description**: Create a book and store it in the database. Takes specified fields in the request payload.

### 5. `book/review`
- **Method**: POST
- **Header**: Authorization
- **Request**: book_id, user_id, review, rating
- **Description**: Upload a review for a book by a user.

### 6. `book/review`
- **Method**: PUT
- **Header**: Authorization
- **Request**: review_id, review, rating
- **Description**: Update the existing review of the user on the book. Users can only update their own reviews.

### 7. `book/review`
- **Method**: DELETE
- **Header**: Authorization
- **Request**: review_id, review, rating
- **Description**: Delete the existing review of the user on the book. Users can only delete their own reviews.

### 8. `book/add-comment-on-review`
- **Method**: POST
- **Header**: Authorization
- **Request**: user_id, review_id, comment
- **Description**: Upload a comment on a review.

### 9. `user/register`
- **Method**: POST
- **Request**: first_name, last_name, is_admin, password, email
- **Description**: Create a user in the system. Hashes the password using the bcrypt library and stores it in the database. The `is_admin` boolean field is used to determine if the user is an admin.

### 10. `user/login`
- **Method**: POST
- **Request**: email, password
- **Description**: Log in a user. Hashes the password using bcrypt and validates it with the stored hashed password in the database. Returns a JWT token that must be sent in the Authorization header for subsequent API access.

### 11. `user/get-users`
- **Method**: GET
- **Header**: Authorization
- **Description**: Return all users from the system. Only admin users can access this.

### 12. `user/delete-users`
- **Method**: DELETE
- **Header**: Authorization
- **Query Params**: user_id
- **Description**: Admin users can delete users from the system.

### 13. `user/change-user-authorization`
- **Method**: PUT
- **Header**: Authorization
- **Query Params**: user_id, change_is_admin
- **Description**: Admins can change any user's authorization.


1. **Source Code:**
   You can find the source code on GitHub at the following link:
   [Adgency AI Assignment - Source Code](https://github.com/sidddhesh100/adgency-ai-assingment)

2. **Database Schema:**
   The database schema is available in the following Google Drive link:
   [Adgency AI Assignment - Database Schema](https://drive.google.com/file/d/1WzEBJVSF5_ictBs9Ks-10Md_DSrb-spX/view?usp=sharing)

3. **Postman Collection:**
   The Postman Collection is included in the GitHub report. Please locate it in the above source code link and import it into Postman for testing.

4. **Deployment:**
   The service has been deployed using AWS EC2. You can access the service through the following root URL:
   [Adgency AI Assignment - Service URL](http://13.112.225.109/)


**Note**: If you have any reviews or suggestions, please reach out via email at siddheshangane142000@gmail.com. Your feedback is valuable!
