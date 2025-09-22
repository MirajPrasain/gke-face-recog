/*
 * Copyright 2023 Google Inc. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
 
document.addEventListener("DOMContentLoaded", function(event) {
  // Login client-side validation
  var login = document.querySelector("#login-form");
  login.addEventListener("submit", function(e) {
    if(!login.checkValidity()){
      e.preventDefault();
      e.stopPropagation();
    }
    login.classList.add('was-validated');
  });

  var showAlert = (window.location.search == "?msg=Login+Failed");
  if (showAlert){
      document.querySelector("#alertBanner").classList.remove("hidden");
  }
});

// Face Recognition Functions
function startFaceRecognition() {
  document.getElementById('faceImageInput').click();
}

function handleFaceImage() {
  const fileInput = document.getElementById('faceImageInput');
  const file = fileInput.files[0];
  
  if (!file) {
    showFaceRecognitionAlert('No image selected', 'danger');
    return;
  }
  
  // Show loading state
  showFaceRecognitionAlert('Processing face recognition...', 'info');
  
  const formData = new FormData();
  formData.append('image', file);
  
  fetch('/facerecog', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    if (data.recognized) {
      showFaceRecognitionAlert(`Welcome ${data.username}! Redirecting...`, 'success');
      // Redirect to home after successful recognition
      setTimeout(() => {
        window.location.href = '/home';
      }, 2000);
    } else {
      showFaceRecognitionAlert('Face not recognized. Please try again.', 'danger');
    }
  })
  .catch(error => {
    console.error('Error:', error);
    showFaceRecognitionAlert('Face recognition failed. Please try again.', 'danger');
  })
  .finally(() => {
    // Reset file input
    fileInput.value = '';
  });
}

function showFaceRecognitionAlert(message, type) {
  const alertBanner = document.querySelector("#alertBanner");
  alertBanner.textContent = message;
  alertBanner.className = `alert alert-${type} mb-4`;
  alertBanner.classList.remove("hidden");
  
  // Auto-hide success messages
  if (type === 'success') {
    setTimeout(() => {
      alertBanner.classList.add("hidden");
    }, 3000);
  }
}