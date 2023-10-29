document.getElementById("form").addEventListener('submit', async function (e) {
    e.preventDefault();
 
    const url = 'https://virtual-try-on2.p.rapidapi.com/clothes-virtual-tryon';
 
    const userImage = document.getElementById('userImage').files[0];
    const jerseyImage = document.getElementById('jerseyImage').files[0];
    const data = new FormData();
 
    data.append("personImage", userImage);
 
    data.append("clothImage", jerseyImage);
 
 
 
    const options = {
 
       method: 'POST',
 
       headers: {
 
          'X-RapidAPI-Key': '0aef1a90a5msh820ce2615965e50p10efd3jsnfccc4667887d',
 
          'X-RapidAPI-Host': 'virtual-try-on2.p.rapidapi.com'
 
       },
 
       body: data
 
    };
 
 
 
    fetch(url, options)
 
       .then(response => response.json())
 
       .then((blob) => {
          const imageData = blob.response.ouput_path_img;
          const imageElement = document.getElementById("my-image");
           imageElement.setAttribute("src", imageData);
       })
 
       .catch(err => console.error(err));
 
 
 })