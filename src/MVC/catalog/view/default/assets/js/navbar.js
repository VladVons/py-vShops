function bootnavbar(options) {
  const defaultOption = {
    selector: "viMainNavbar"
  };

  const bnOptions = { ...defaultOption, ...options };

  init = function () {
    var dropdowns = document.getElementById(bnOptions.selector).getElementsByClassName("dropdown");

    Array.prototype.forEach.call(dropdowns, (item) => {
      item.addEventListener("mouseover", function () {
        this.classList.add("show");
        const element = this.querySelector(".dropdown-menu");
        element.classList.add("show");
      });

      item.addEventListener("mouseout", function () {
        this.classList.remove("show");
        const element = this.querySelector(".dropdown-menu");
        element.classList.remove("show");
      });
    });
  };

  init();
}

new bootnavbar();
