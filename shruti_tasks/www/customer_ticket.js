document.getElementById('ticket-form').addEventListener('submit', function (e) {
    e.preventDefault();

    clearErrors();

    let isValid = true;

    // Helper Functions
    function showError(input, message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.style.color = 'red';
        errorDiv.style.fontSize = '0.9em';
        errorDiv.textContent = message;
        input.parentNode.appendChild(errorDiv);
    }

    function clearErrors() {
        const existingErrors = document.querySelectorAll('.error-message');
        existingErrors.forEach(error => error.remove());
    }

    // Validate Customer Name
    const customerNameInput = document.getElementById('customer-name');
    const customerName = customerNameInput.value.trim();

    if (!customerName) {
        showError(customerNameInput, 'Customer name is required');
        isValid = false;
    } else if (!/^[A-Za-z\s]+$/.test(customerName)) {
        showError(customerNameInput, 'Name should contain only alphabets and spaces');
        isValid = false;
    }

    // Validate Email
    const emailInput = document.getElementById('email');
    const email = emailInput.value.trim();

    if (!email) {
        showError(emailInput, 'Email is required');
        isValid = false;
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        showError(emailInput, 'Please enter a valid email address');
        isValid = false;
    }

    // Validate Category
    const categoryInput = document.getElementById('category');
    const category = categoryInput.value;

    if (!category) {
        showError(categoryInput, 'Please select a category');
        isValid = false;
    }

    // Validate Description
    const descriptionInput = document.getElementById('description');
    const descriptionValue = descriptionInput.value.trim();

    if (!descriptionValue) {
        showError(descriptionInput, 'Description is required');
        isValid = false;
    }

    // Validate Phone (if provided)
    const phoneInput = document.getElementById('phone');
    const phone = phoneInput.value.trim();

    if (phone && !/^\d{10}$/.test(phone)) {
        showError(phoneInput, 'Phone number must be exactly 10 digits without spaces or special characters');
        isValid = false;
    }

    // Proceed only if all validations pass
    if (!isValid) return;


    const formData = new FormData();

    const nonFileFields = ['csrf_token', 'customerName', 'email', 'phone', 'category', 'description','resolutionNotes'];
    nonFileFields.forEach(field => {
        const fieldValue = document.querySelector(`[name="${field}"]`).value;
        if (fieldValue) {
            formData.append(field, fieldValue);
        }
    });


    // Log FormData for debugging
    formData.forEach((value, key) => {
        console.log(`${key}:`, value);
    });

    // Send form data via Fetch API
    fetch('/api/method/shruti_tasks.www.customer_ticket.save_ticket', {
        method: 'POST',
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            console.log("333",data)
            console.log("******",data.message.message)

            alert('Ticket submitted successfully!');
            document.getElementById('ticket-form').reset();
            // if(data.message.message === "Ticket submitted successfully!"){
            //     alert('Ticket submitted successfully!');
            //     document.getElementById('ticket-form').reset();
            // }
      
        })
        // .catch(error => {
        //     console.error('Error:', error);
        //     alert('An error occurred while submitting the ticket.');
        // });
});
