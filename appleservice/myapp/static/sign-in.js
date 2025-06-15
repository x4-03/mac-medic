document.addEventListener("DOMContentLoaded", () => {
  const proceedBtn = document.getElementById("proceedBtn");

  const fields = {
    firstName: document.getElementById("firstName"),
    lastName: document.getElementById("lastName"),
    email: document.getElementById("email"),
    password: document.getElementById("password"),
    phone: document.getElementById("phone"),
  };

  function highlightField(field, isValid) {
    field.classList.remove("invalid", "valid");
    field.classList.add(isValid ? "valid" : "invalid");
  }

  function validateFields() {
    let allValid = true;

    // Regex patterns
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const phoneRegex = /^\+48\d{9}$/;

    // Validate each field
    const validations = {
      firstName: fields.firstName.value.trim() !== "",
      lastName: fields.lastName.value.trim() !== "",
      email: emailRegex.test(fields.email.value.trim()),
      password: fields.password.value.length >= 8 && fields.password.value.length <= 20,
      phone:
        fields.phone.value.trim() === "" || phoneRegex.test(fields.phone.value.trim()),
    };

    // Highlight each field
    for (const [key, isValid] of Object.entries(validations)) {
      highlightField(fields[key], isValid);
      if (!isValid) allValid = false;
    }

    return allValid;
  }

  function proceedIfValid() {
    /*if (validateFields()) {
      alert("Pomyślnie utworzono konto!");
    }*/
  }

  proceedBtn.addEventListener("click", proceedIfValid);
  
  var location = document.querySelector("select[name=location]");
  var isWorker = document.querySelector("input[name=is_worker]");
  isWorker.addEventListener('change', function() {
    if (this.checked) {
      location.classList.remove("text-muted")
      location.disabled = false
    } else {
      location.classList.add("text-muted")
      location.disabled = true
    }
  });
});

