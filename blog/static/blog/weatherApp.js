const container = document.querySelector('.container');
const search = document.querySelector('.search-box button');
const weatherBox = document.querySelector('.weather-box');
const weatherDetails = document.querySelector('.weather-details');
const error404 = document.querySelector('.not-found');

// Add event listener for the search button click event
search.addEventListener('click', () => {
    // Retrieve the city name from the input field
    const city = document.querySelector('.search-box input').value;
    
    if (city === '') return;

    // Fetch weather data from the weather API
    fetch(`http://api.weatherapi.com/v1/current.json?key=98c11e6802514f0fbdf170048242804&q=${city}&aqi=no`)
        .then(response => response.json()) // Parse JSON response into a JavaScript object
        .then(json => {
            // Check if the API returned an error (e.g., city not found)
            if (json.error) {
                // Adjust UI to show error state
                container.style.height = '400px';
                weatherBox.style.display = 'none';
                weatherDetails.style.display = 'none';
                error404.style.display = 'block';
                error404.classList.add('fadeIn'); 
                return;
            }

            // If no error, hide the error message and remove any animation classes
            error404.style.display = 'none';
            error404.classList.remove('fadeIn');

            // Select and update individual weather information elements
            const temperature = weatherBox.querySelector('.temperature');
            const description = weatherBox.querySelector('.description');
            const humidity = weatherDetails.querySelector('.humidity span');
            const wind = weatherDetails.querySelector('.wind span');

            // Display the weather data in the UI
            temperature.innerHTML = `${parseInt(json.current.temp_c)}<span>°C</span>`;
            description.innerHTML = `${json.current.condition.text}`;
            humidity.innerHTML = `${json.current.humidity}%`;
            wind.innerHTML = `${parseInt(json.current.wind_kph)}Km/h`;

            // Make the weather data boxes visible and adjust the main container's height
            weatherBox.style.display = '';
            weatherDetails.style.display = '';
            weatherBox.classList.add('fadeIn');
            weatherDetails.classList.add('fadeIn');
            container.style.height = '590px';
        })
        .catch(error => {
            // Log and display errors if the API call fails
            console.error('Error fetching data:', error);
            container.style.height = '400px';
            weatherBox.style.display = 'none';
            weatherDetails.style.display = 'none';
            error404.style.display = 'block';
            error404.classList.add('fadeIn');
        });
});
