// proteccion Visual 

  document.addEventListener('DOMContentLoaded', () => {
    const modoGuardado = localStorage.getItem('modo');
    const body = document.body;
    const btn = document.getElementById('modoToggle');

    if (modoGuardado === 'oscuro') {
      body.classList.add('modo-oscuro');
    } else {
      body.classList.add('modo-claro');
    }
  });

  function cambiarModo() {
    const body = document.body;
    const btn = document.getElementById('modoToggle');

    if (body.classList.contains('modo-oscuro')) {
      body.classList.replace('modo-oscuro', 'modo-claro');
      localStorage.setItem('modo', 'claro');
    } else {
      body.classList.replace('modo-claro', 'modo-oscuro');
      localStorage.setItem('modo', 'oscuro');
    }
  }

  
//Scroll de galeria Carrucel (EnConstruccion!!)
window.onscroll = function () {
    const btn = document.getElementById("btnSubir");
    if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
      btn.classList.add("mostrar");
    } else {
      btn.classList.remove("mostrar");
    }
  };
  
  function scrollArriba() {
    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
  }

  function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    if (sidebar.style.width === "250px") {
      sidebar.style.width = "0";
    } else {
      sidebar.style.width = "250px";
    }
  }
 //////////////////////////////////////////////////////////////////////////////////////////// 
  
//   ////////////////////////// No tocar esta seccion///////////////////////////////////////////
  let startX = 0;
  
  document.addEventListener('touchstart', (e) => {
    startX = e.touches[0].clientX;
  });
  
  document.addEventListener('touchend', (e) => {
    let endX = e.changedTouches[0].clientX;
    if (startX < 50 && endX - startX > 100) {
      toggleSidebar();
    }
  });
/////////////////////////////////////////////////////////////////////////////////////////////


  //Funcion de mostar Alerta (Terminada)
  function mostrarAlerta() {
    const alerta = document.getElementById("alerta");
    alerta.classList.remove("oculto");
    alerta.classList.add("mostrar");
  
    setTimeout(() => {
      cerrarAlerta();
    }, 5000);
  }
  
  //Funcion de Cerrar alerta (En construccion)
  function cerrarAlerta() {
    const alerta = document.getElementById("alerta");
    alerta.classList.remove("mostrar");
    setTimeout(() => {
      alerta.classList.add("oculto");
    }, 500); 
  }


  //------------------------------------js de bootstrap/templatesWeb de prueba y ejemplo -----------------------------------
  const slides = document.getElementById('slides')
  const total = slides.children.length
  let index = 0
  let interval = setInterval(autoSlide, 3000)
  
  function showSlide(i) {
    index = (i + total) % total
    slides.style.transform = `translateX(-${index * 100}%)`
  }
  
  function nextSlide() {
    showSlide(index + 1)
    resetInterval()
  }
  
  function prevSlide() {
    showSlide(index - 1)
    resetInterval()
  }
  
  function autoSlide() {
    showSlide(index + 1)
  }
  
  function resetInterval() {
    clearInterval(interval)
    interval = setInterval(autoSlide, 3000)
  }

  // maquetado login-alerta (En Construccion)
  function validarLogin() {
    const correo = document.getElementById('correo').value
    const clave = document.getElementById('clave').value
    if (!correo || !clave) {
      alert('Por favor, completa todos los campos.')
      return
    }
    alert(`Bienvenid@ ${correo}`)
  }
  
  function enviarMensaje() {
    const input = document.getElementById('mensaje')
    const chatBox = document.getElementById('chatBox')
    if (input.value.trim() !== '') {
      const nuevoMensaje = document.createElement('div')
      nuevoMensaje.textContent = input.value
      chatBox.appendChild(nuevoMensaje)
      input.value = ''
      chatBox.scrollTop = chatBox.scrollHeight
    }
  }









  // ////////////////////////////////////////////////////////////




  
  
  function toggleModo() {
    const body = document.body;
    const icono = document.getElementById("icono-modo");
    const btn = document.getElementById("modo-btn");

    if (body.classList.contains("bg-light")) {
      body.classList.replace("bg-light", "bg-dark");
      body.classList.add("text-white");
      icono.classList.replace("bi-moon-stars", "bi-sun");
      btn.classList.replace("btn-dark", "btn-light");

      localStorage.setItem("modo", "oscuro");  // Guardar preferencia
    } else {
      body.classList.replace("bg-dark", "bg-light");
      body.classList.remove("text-white");
      icono.classList.replace("bi-sun", "bi-moon-stars");
      btn.classList.replace("btn-light", "btn-dark");

      localStorage.setItem("modo", "claro");  // Guardar preferencia
    }
  }

  // Aplicar modo guardado al cargar la página
  window.onload = function () {
    const modoGuardado = localStorage.getItem("modo");
    const body = document.body;
    const icono = document.getElementById("icono-modo");
    const btn = document.getElementById("modo-btn");

    if (modoGuardado === "oscuro") {
      body.classList.replace("bg-light", "bg-dark");
      body.classList.add("text-white");
      icono.classList.replace("bi-moon-stars", "bi-sun");
      btn.classList.replace("btn-dark", "btn-light");
    } else {
      body.classList.replace("bg-dark", "bg-light");
      body.classList.remove("text-white");
      icono.classList.replace("bi-sun", "bi-moon-stars");
      btn.classList.replace("btn-light", "btn-dark");
    }
  };



  const listaMensajes = document.getElementById("lista-mensajes");
  listaMensajes.innerHTML = "";

  if (mensajes.length === 0) {
    listaMensajes.innerHTML = '<li class="list-group-item">No hay mensajes recientes.</li>';
  } else {
    mensajes.forEach(({cliente, correo, telefono, mensaje}) => {
      const li = document.createElement("li");
      li.className = "list-group-item";
      li.innerHTML = `
        <strong>${cliente}</strong><br />
        <em>${mensaje}</em>
        <div class="detalle-contacto">
          Correo: <a href="mailto:${correo}">${correo}</a> | Tel: <a href="tel:${telefono}">${telefono}</a>
        </div>
      `;
      listaMensajes.appendChild(li);
    });
  }

  // Ejemplo para actualizar números dinámico JS
  // Simulación de datos
  const totalClientes = 35;
  const propiedadesPorTipo = {
    Casa: 60,
    Departamento: 70,
    Terreno: 20,
  };

  // Actualizar total Clientes
  document.getElementById('total-clientes').textContent = totalClientes;

  // Actualizar total propiedades por Tipo
  const listaPropiedades = document.getElementById('total-propiedades-tipo');
  for (const [tipo, cantidad] of Object.entries(propiedadesPorTipo)) {
    const li = [...listaPropiedades.children].find(li => li.textContent.includes(tipo));
    if (li) {
      li.querySelector('span').textContent = cantidad;
    }
  }

