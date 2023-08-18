document.addEventListener('DOMContentLoaded', function () {
  const emailInput = document.getElementById('mail');
  const passwordInput = document.getElementById('pd');
  const confirmPasswordInput = document.getElementById('cmpwd');
  //const aadhaarInput = document.getElementById('adnumber');
  const nameInput = document.getElementById('vname');
  const form = document.getElementById('regform');

  // Function to validate email
  function validateEmail() {
    const emailError = document.getElementById('emailError');

    if (!isValidEmail(emailInput.value)) {
      emailInput.classList.add('is-invalid');
      emailError.innerText = 'Please enter a valid email address.';
    } else {
      emailInput.classList.remove('is-invalid');
      emailError.innerText = '';
    }
  }

  // Function to validate password
  function validatePassword() {
    const passwordError = document.getElementById('passwordError');
    const password = passwordInput.value;

    const errors = [];
    if (password.length < 6) {
      errors.push('Password must be at least 6 characters long.');
    }
    if (!containsUppercase(password)) {
      errors.push('Password must contain at least one uppercase letter.');
    }
    if (!containsLowercase(password)) {
      errors.push('Password must contain at least one lowercase letter.');
    }
    if (!containsSpecialCharacter(password)) {
      errors.push('Password must contain at least one special character.');
    }
    if(!containsNumber(password)) {
      errors.push('Password must contain at least one number character.');
    }

    if (errors.length > 0) {
      passwordInput.classList.add('is-invalid');
      passwordError.innerText = errors.join(' ');
    } else {
      passwordInput.classList.remove('is-invalid');
      passwordError.innerText = '';
    }

    validateConfirmPassword();
  }

  // Function to validate confirm password
  function validateConfirmPassword() {
    const confirmPasswordError = document.getElementById('confirmPasswordError');

    if (confirmPasswordInput.value !== passwordInput.value) {
      confirmPasswordInput.classList.add('is-invalid');
      confirmPasswordError.innerText = 'Passwords do not match.';
    } else {
      confirmPasswordInput.classList.remove('is-invalid');
      confirmPasswordError.innerText = '';
    }
  }

  function validateName() {
    const nameError = document.getElementById('nameError');
    const name = nameInput.value.trim();
    const namePattern = /^[a-zA-Z ]+$/;

    if (!namePattern.test(name)) {
      nameInput.classList.add('is-invalid');
      nameError.innerText = 'Please enter a valid name.';
    } else {
      nameInput.classList.remove('is-invalid');
      nameError.innerText = '';
    }
  }

    // Function to validate aadhaar number
    function validateAadhaar(aadhaarInput) {
      // Check if Aadhaar number is exactly 12 digits
      if (!/^\d{12}$/.test(aadhaarInput)) {
          return false;
      }
  
      // Check for the checksum using Verhoeff algorithm
      const aadhaarArray = aadhaarInput.split('').map(Number);
      const d = [
          [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
          [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
          [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
          [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
          [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
      ];
      let i = 0;
      let j = 0;
      for (i = 0; i < aadhaarArray.length; i++) {
          j = d[j][d[(i % 4)][aadhaarArray[aadhaarArray.length - 1 - i]]];
      }
  
      return j === 0;
  }

  // Helper functions for validation
  function containsUppercase(text) {
    return /[A-Z]/.test(text);
  }

  function containsLowercase(text) {
    return /[a-z]/.test(text);
  }

  function containsSpecialCharacter(text) {
    return /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(text);
  }

  function isValidEmail(email) {
    const emailRegex = /\S+@\S+\.\S+/;
    return emailRegex.test(email);
  }
  function containsNumber(text) {
    return /[0-9]/.test(text);
  }
  // Event listeners for instant validation
  emailInput.addEventListener('input', validateEmail);
  passwordInput.addEventListener('input', validatePassword);
  confirmPasswordInput.addEventListener('input', validateConfirmPassword);
  nameInput.addEventListener('input', validateName);

  // Form submit event listener for final validation before submission
  form.addEventListener('submit', function (event) {
    validateEmail();
    validatePassword();
    validateConfirmPassword();
    validateName();

    if (emailInput.classList.contains('is-invalid') || passwordInput.classList.contains('is-invalid') || nameInput.classList.contains('is-invalid')){
      event.preventDefault();
    }
  });
});
