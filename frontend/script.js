document.addEventListener('DOMContentLoaded', () => {

    const eventsContainer = document.getElementById('events');

    const socket = new WebSocket('ws://127.0.0.1:8001/ws/events/');

    socket.onopen = function() {
        console.log('WebSocket соединение открыто');
    };

    socket.onmessage = function(event) {
        console.log('Получено сообщение по WebSocket:', event.data);
        const data = JSON.parse(event.data);
        updateEventsList([data]);
        showEventDetails(data);
    };

    socket.onerror = function(error) {
        console.error('Ошибка WebSocket:', error);
    };

    socket.onclose = function() {
        console.log('WebSocket соединение закрыто');
    };

    async function fetchEvents() {
        console.log('Запрос данных событий с сервера');
        try {
            const response = await fetch('http://127.0.0.1:8000/api/event/?format=json',
                 {
                    method: "GET",
                    headers: {
                        "X-Requested-With": "XMLHttpRequest",
                    }
                }
            );
            if (response.ok) {
                const events = await response.json();
                console.log('Получены данные событий:', events);
                updateEventsList(events);
            } else {
                console.error('Ошибка при получении данных событий');
            }
        } catch (error) {
            console.error('Ошибка при запросе данных событий:', error);
        }
    }

    function updateEventsList(events) {
        console.log('Обновление списка событий:', events);
        eventsContainer.innerHTML = '';  // Очищаем текущий список

        const ul = document.createElement('ul');
        ul.classList.add('events-list');

        events.forEach((event, index) => {
            const li = document.createElement('li');
            li.classList.add('event-item');
            li.dataset.index = index; // Сохраняем индекс события

            const title = document.createElement('h3');
            title.textContent = event.description || `Событие ${index + 1}`;

            const description = document.createElement('p');
            description.textContent = event.timestamp;

            const image = document.createElement('img');
            image.src = `${event.image}`;
            image.alt = 'Фото события'

            li.appendChild(title);
            li.appendChild(description);
            li.appendChild(image);

            ul.appendChild(li);

            li.addEventListener('click', () => showEventDetails(event));
        });

        eventsContainer.appendChild(ul);
    }
    fetchEvents();
    setInterval(fetchEvents, 500000);  // Запрашиваем данные каждые 5 секунд


    const navLinks = document.querySelectorAll('nav a[data-section]');
    const sectionsContainer = document.querySelector('.sections-container');
    let allSections = document.querySelectorAll('.section'); // Используем let

    const yStep = 150; // каждая следующая секция на 150px выше предыдущей
    const zStep = -1500; // каждая следующая секция на 1500px дальше по оси Z
    const tiltAngle = -5; // градусов

    // Добавляем класс к секции на основе её data-section
    allSections.forEach(sec => {
        const secName = sec.getAttribute('data-section');
        if (secName) {
            sec.classList.add(secName);
        }
    });

    // Расставляем секции по "лестнице"
    allSections.forEach((sec, index) => {
        const translateYValue = -(index * yStep);
        const translateZValue = (index * zStep);
        sec.style.transform = `translateY(${translateYValue}px) translateZ(${translateZValue}px) rotateX(${tiltAngle}deg)`;
        sec.style.opacity = '0.5';
        sec.style.zIndex = `${-index}`;
        sec.style.visibility = 'hidden';
    });

    function showSection(targetSectionName) {
        console.log('Показ секции:', targetSectionName);
        const allSections = document.querySelectorAll('.section');
        allSections.forEach((sec, index) => {
            sec.classList.remove('active');
            sec.style.opacity = '0.5';
            sec.style.zIndex = `${-index}`;
            sec.style.visibility = 'visible';
            const translateYValue = -(index * yStep);
            const translateZValue = (index * zStep);
            sec.style.transform = `translateY(${translateYValue}px) translateZ(${translateZValue}px) rotateX(${tiltAngle}deg)`;
        });

        const activeSection = document.querySelector(`.section[data-section="${targetSectionName}"]`);
        if (activeSection) {
            console.log('Найденная активная секция:', activeSection);
            activeSection.classList.add('active');
            activeSection.style.opacity = '1';
            activeSection.style.visibility = 'visible';

            const sectionIndex = Array.from(allSections).indexOf(activeSection);
            allSections.forEach((sec, index) => {
                if (sec === activeSection) {
                    sec.style.zIndex = allSections.length; // активная секция всегда впереди
                } else {
                    sec.style.zIndex = `${-index}`; // неактивные секции позади
                }
            });

            const containerTranslateY = (sectionIndex * yStep);
            const containerTranslateZ = -(sectionIndex * zStep);
            sectionsContainer.style.transform = `translateY(${containerTranslateY}px) translateZ(${containerTranslateZ}px)`;
            allSections.forEach((sec, idx) => {
                sec.style.opacity = (idx === sectionIndex) ? '1' : '0.1';
            });
        } else {
            console.error("No section found for:", targetSectionName);
        }
    }

    // Функция для отображения событий как списка внутри events-section
    // function displayEventsList(events) {
    //     console.log('Отображение событий как списка:', events);
    //     const eventsContainer = document.getElementById('events');
        
    //     if (!eventsContainer) {
    //         console.error('Контейнер для событий не найден');
    //         return;
    //     }

    //     // Создаём список
    //     const ul = document.createElement('ul');
    //     ul.classList.add('events-list');

    //     events.forEach((event, index) => {
    //         console.log(`Создание элемента списка для события ${index + 1}:`, event);

    //         // Создаём элемент списка
    //         const li = document.createElement('li');
    //         li.classList.add('event-item');

    //         // Добавляем содержимое события
    //         const title = document.createElement('h3');
    //         title.textContent = event.title || `Событие ${index + 1}`;

    //         const description = document.createElement('p');
    //         description.textContent = event.description || 'Описание события.';
            
    //         li.appendChild(title);
    //         li.appendChild(description);

    //         ul.appendChild(li);

    //         // Добавляем обработчик клика для открытия события с фото
    //         li.addEventListener('click', () => showEventDetails(event));
    //     });

    //     // Добавляем список в контейнер
    //     eventsContainer.appendChild(ul);
    // }

    function showEventDetails(event) {
        console.log('Показ деталей события:', event);
        // Найдём или создадим контейнер для деталей события
        let detailsContainer = document.querySelector('.event-details-section');
        if (!detailsContainer) {
            detailsContainer = document.createElement('div');
            detailsContainer.classList.add('section', 'event-details-section');
            detailsContainer.setAttribute('data-section', 'event-details');
            sectionsContainer.appendChild(detailsContainer);
        }
    
        detailsContainer.innerHTML = ''; // Очистим предыдущий контент
    
        const detailsContent = document.createElement('div');
        detailsContent.classList.add('event-details');
    
        const title = document.createElement('h2');
        title.textContent = event.title || 'Детали события';
    
        const description = document.createElement('p');
        description.textContent = event.description || 'Описание события.';
    
        const imageContainer = document.createElement('div');
        imageContainer.classList.add('image-container');
        imageContainer.style.overflow = 'auto';
        imageContainer.style.maxHeight = '400px'; // Ограничиваем высоту контейнера изображений
    
        const image = document.createElement('img');
        image.src = `${event.image}`;
        image.alt = 'Фото события';
    
        imageContainer.appendChild(image);
        detailsContent.appendChild(title);
        detailsContent.appendChild(description);
        detailsContent.appendChild(imageContainer);
    
        // Добавляем кнопку для возврата к списку
        const backButton = document.createElement('button');
        backButton.textContent = 'Назад к списку событий';
        backButton.addEventListener('click', () => {
            detailsContainer.style.display = 'none'; // Скрываем контейнер с деталями события
            const eventsContainer = document.getElementById('events');
            eventsContainer.style.display = 'block'; // Показываем список событий
            showSection('events-0'); // Возвращаемся к секции событий
        });
    
        detailsContent.appendChild(backButton);
        detailsContainer.appendChild(detailsContent);
    
        // Скрываем список событий и показываем детали события
        const eventsContainer = document.getElementById('events');
        eventsContainer.style.display = 'none';
        detailsContainer.style.display = 'flex';
    
        // Показываем секцию с деталями события
        showSection('event-details');
    }

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetSection = link.getAttribute('data-section');
            showSection(targetSection);
        });
    });

    const uploadForm = document.getElementById('uploadForm');

    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        console.log('Начало загрузки видео...');
        const formData = new FormData(uploadForm);
        const videoFile = formData.get('video');
        
        try {
            const response = await fetch('http://127.0.0.1:8000/api/upload-video/', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const result = await response.json();
                console.log(result.message);
                alert(result.message);
            } else {
                console.error('Ошибка загрузки видео');
                alert('Ошибка загрузки видео');
            }
        } catch (error) {
            console.error('Ошибка:', error);
        }
    });

    

    showSection('home');

    window.addEventListener('resize', () => {
        // Можно добавить логику для пересчета yStep и zStep при изменении размера окна.
    });
    console.log('Начало выполнения fetch запроса');
});
