
# Things to consider when applying CSS to files


## Thing One:

In `templates/signup.html`, the input fields of the signup form can NOT be assigned
an `id` or `class` attribute, because of the way they are rendered, is such that the 
applied CSS will have NO effect if page reloads after invalid inputs.
### Solution: 
Assign an `id` to the main form, as it is not dynamic, and target the input elements from
the form using its' `id` attribute.