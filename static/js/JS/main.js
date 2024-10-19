// script.js

document.getElementById("menuToggle").addEventListener("click", function () {
  var dropdownMenu = document.getElementById("dropdownMenu");
  var menuToggleIcon = this.querySelector("i");
  if (dropdownMenu.style.display === "flex") {
    dropdownMenu.style.display = "none";
    this.innerHTML = 'Menu <i class="fa-solid fa-bars"></i>';
  } else {
    dropdownMenu.style.display = "flex";
    this.innerHTML = 'Close <i class="fa-solid fa-times"></i>';
  }
});
document.addEventListener("click", function (event) {
  var dropdownMenu = document.getElementById("dropdownMenu");
  var menuToggle = document.getElementById("menuToggle");
  if (
    dropdownMenu.style.display === "flex" &&
    !menuToggle.contains(event.target) &&
    !dropdownMenu.contains(event.target)
  ) {
    dropdownMenu.style.display = "none";
    menuToggle.innerHTML = 'Menu <i class="fa-solid fa-bars"></i>';
  }
});
// Close the dropdown menu when any option is clicked
// Close the dropdown menu on mobile screens when an option is clicked
function handleMenuOptionClick(event) {
  if (window.innerWidth <= 768) {
    var menuOption = event.target;
    if (menuOption.id !== "loginToggle") {
      var dropdownMenu = document.getElementById("dropdownMenu");
      var menuToggle = document.getElementById("menuToggle");
      dropdownMenu.style.display = "none";
      menuToggle.textContent = "Menu";
    }
  }
}
document.querySelectorAll(".menu li a").forEach(function (menuOption) {
  menuOption.addEventListener("click", handleMenuOptionClick);
});

document.addEventListener("DOMContentLoaded", function () {
  var popup = document.getElementById("popup");
  var closeBtn = document.querySelector(".close-btn");

  if (!popup || !closeBtn) {
    console.error("One or more elements are not found.");
    return;
  }

  closeBtn.addEventListener("click", function () {
    popup.style.display = "none";
  });

  window.addEventListener("click", function (event) {
    if (event.target === popup) {
      popup.style.display = "none";
    }
  });
});

// script.js

document.getElementById("readMoreBtn").addEventListener("click", function () {
  var content = document.querySelector(".content");
  content.classList.toggle("expanded");
  var btn = document.getElementById("readMoreBtn");
  if (content.classList.contains("expanded")) {
    btn.textContent = "Read Less";
  } else {
    btn.textContent = "Read More";
  }
});

document.getElementById("readMoreBtn").addEventListener("click", function () {
  var content = document.querySelector(".talk");
  content.classList.toggle("expanded");
  var btn = document.getElementById("readMoreBtn");
  if (content.classList.contains("expanded")) {
    btn.textContent = "Read Less";
  } else {
    btn.textContent = "Read More";
  }
});
document.addEventListener("DOMContentLoaded", () => {
  const counters = document.querySelectorAll(".counter");
  const speed = 500; // The lower the number, the faster the count

  const startCounting = (counter) => {
    const updateCount = () => {
      const target = +counter.getAttribute("data-target");
      const count = +counter.innerText;

      // Lower increment to slow and higher to speed
      const increment = target / speed;

      // Check if target is reached
      if (count < target) {
        // Add increment
        counter.innerText = Math.ceil(count + increment);
        // Call function every 1 millisecond
        setTimeout(updateCount, 1);
      } else {
        counter.innerText = target;
      }
    };

    updateCount();
  };

  const observerOptions = {
    root: null, // Use the viewport as the root
    rootMargin: "0px",
    threshold: 0.1, // When 10% of the element is visible
  };

  const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const counter = entry.target;
        startCounting(counter);
        observer.unobserve(counter); // Stop observing once started
      }
    });
  }, observerOptions);

  counters.forEach((counter) => {
    observer.observe(counter);
  });
});
document.addEventListener("DOMContentLoaded", () => {
  const counters = document.querySelectorAll(".counter");
  const animatables = document.querySelectorAll(".animatable"); // Select elements to animate
  const speed = 500; // The lower the number, the faster the count

  const startCounting = (counter) => {
    const updateCount = () => {
      const target = +counter.getAttribute("data-target");
      const count = +counter.innerText;

      // Lower increment to slow and higher to speed
      const increment = target / speed;

      // Check if target is reached
      if (count < target) {
        // Add increment
        counter.innerText = Math.ceil(count + increment);
        // Call function every 1 millisecond
        setTimeout(updateCount, 1);
      } else {
        counter.innerText = target;
      }
    };

    updateCount();
  };

  const observerOptions = {
    root: null, // Use the viewport as the root
    rootMargin: "0px",
    threshold: 0.1, // When 10% of the element is visible
  };

  const handleIntersection = (entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        if (entry.target.classList.contains("counter")) {
          startCounting(entry.target);
        } else if (entry.target.classList.contains("animatable")) {
          entry.target.classList.add("animated", "fadeInUp");
        }
        observer.unobserve(entry.target); // Stop observing once started
      }
    });
  };

  const observer = new IntersectionObserver(
    handleIntersection,
    observerOptions
  );

  counters.forEach((counter) => {
    observer.observe(counter);
  });

  animatables.forEach((animatable) => {
    observer.observe(animatable);
  });
});
document.addEventListener("DOMContentLoaded", () => {
  const menuToggle = document.getElementById("menuToggle");
  const dropdownMenu = document.getElementById("dropdownMenu");
  const loginToggle = document.getElementById("loginToggle");
  const loginDropdown = document.getElementById("loginDropdown");

  // Toggle login submenu
  loginToggle.addEventListener("click", (event) => {
    event.preventDefault(); // Prevent default anchor behavior
    loginDropdown.style.display =
      loginDropdown.style.display === "block" ? "none" : "block";
  });

  // Close menus when clicking outside
  document.addEventListener("click", (event) => {
    if (!event.target.closest(".dropdownmenu")) {
      loginDropdown.style.display = "none";
    }
  });
});
document
  .getElementById("noticeLink")
  .addEventListener("click", function (event) {
    event.preventDefault();
    document.getElementById("notice").scrollIntoView({ behavior: "smooth" });
  });


  
function updateHeaderHeight() {
  var header = document.querySelector("header");
  var headerHeight = header.offsetHeight;
  document.documentElement.style.setProperty(
    "--header-height",
    `${headerHeight}px`
  );
}

// Update the height on initial load
document.addEventListener("DOMContentLoaded", updateHeaderHeight);

// Optionally, update the height on window resize
window.addEventListener("resize", updateHeaderHeight);

// document.addEventListener("DOMContentLoaded", function () {
//   const header = document.querySelector("header");

//   window.addEventListener("scroll", function () {
//     if (window.scrollY > 0) {
//       header.classList.add("header-no-padding");
//     } else {
//       header.classList.remove("header-no-padding");
//   }
// });
// });

document.addEventListener("DOMContentLoaded", function () {
  const header = document.querySelector("header");
  const contact = document.querySelector(".contact");

  window.addEventListener("scroll", function () {
    if (window.scrollY > 0) {
      header.classList.add("header-no-padding");
      contact.classList.add("contact-no-margin");
    } else {
      header.classList.remove("header-no-padding");
      contact.classList.remove("contact-no-margin");
}
});
});
