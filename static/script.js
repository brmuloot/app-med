const form = document.querySelector('#image-form');
const resultDiv = document.querySelector('#result');

form.addEventListener('submit', (event) => {
  event.preventDefault();
  
  const fileInput = document.querySelector('#image');
  const file = fileInput.files[0];
  
  const formData = new FormData();
  formData.append('image', file);

  const reader = new FileReader();
  reader.onload = (event) => {
    const imageUrl = event.target.result;
    const imageElement = document.createElement('img');
    imageElement.src = imageUrl;
    imageElement.width = 400;
    imageElement.height = 300;
    resultDiv.appendChild(imageElement);
  };
  reader.readAsDataURL(file);

  fetch('/apply_model', {
    method: 'POST',
    body: formData
  })
  .then(response => response.text())
  .then(result => {
    resultDiv.innerHTML += `<p>Résultat de la prédiction : ${result}</p>`;
  })
  .catch(error => {
    resultDiv.innerHTML += `<p>Erreur : ${error.message}</p>`;
  });
});
