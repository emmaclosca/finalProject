const container = document.querySelector('.container');
const search = document.querySelector('.search-box button');
const weatherBox = document.querySelector('.weather-box');
const weatherDetails = document.querySelector('.weather-details');
const error404 = document.querySelector('.not-found');

search.addEventListener('click', () => {

    const APIKey = '98c11e6802514f0fbdf170048242804';
    const city = document.querySelector('.search-box input').value;

    if (city === '')
        return;

    fetch(`http://api.weatherapi.com/v1/current.json?key=98c11e6802514f0fbdf170048242804&q=${city}&aqi=no`)
        .then(response => response.json())
        .then(json => {

            if (json.error) {
                container.style.height = '400px';
                weatherBox.style.display = 'none';
                weatherDetails.style.display = 'none';
                error404.style.display = 'block';
                error404.classList.add('fadeIn');

                // Display invalid location message and image
                error404.querySelector('p').textContent = `Oops! Invalid location :/`;
                error404.querySelector('img').src = '{% static "blog/images/404.png" %}';

                return;
            }

            error404.style.display = 'none';
            error404.classList.remove('fadeIn');

            const image = weatherBox.querySelector('img');
            const temperature = weatherBox.querySelector('.temperature');
            const description = weatherBox.querySelector('.description');
            const humidity = weatherDetails.querySelector('.humidity span');
            const wind = weatherDetails.querySelector('.wind span');

            switch (json.current.condition.text) {
                case 'Clear':
                    image.src = 'images/clear.png';
                    break;

                case 'Rain':
                    image.src = 'images/rain.png';
                    break;

                case 'Snow':
                    image.src = 'images/snow.png';
                    break;

                case 'Clouds':
                    image.src = 'images/cloud.png';
                    break;

                case 'Haze':
                    image.src = 'images/mist.png';
                    break;

                default:
                    image.src = '';
            }

            temperature.innerHTML = `${parseInt(json.current.temp_c)}<span>°C</span>`;
            description.innerHTML = `${json.current.condition.text}`;
            humidity.innerHTML = `${json.current.humidity}%`;
            wind.innerHTML = `${parseInt(json.current.wind_kph)}Km/h`;

            weatherBox.style.display = '';
            weatherDetails.style.display = '';
            weatherBox.classList.add('fadeIn');
            weatherDetails.classList.add('fadeIn');
            container.style.height = '590px';
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            container.style.height = '400px';
            weatherBox.style.display = 'none';
            weatherDetails.style.display = 'none';
            error404.style.display = 'block';
            error404.classList.add('fadeIn');

            // Display invalid location message and image
            error404.querySelector('p').textContent = `Oops! Invalid location :/`;
            error404.querySelector('img').src = '{% static "blog/images/404.png" %}';
        });
});
