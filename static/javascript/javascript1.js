const text__1 = document.querySelector(".text__1")
const text__2 = document.querySelector(".text__2")
const box2__item__fazer1 = document.querySelector(".box2__item__fazer1")
const box2__item__fazer2 = document.querySelector(".box2__item__fazer2")

box2__item__fazer1.classList.add("active1")


text__2.addEventListener("click", function () {
    box2__item__fazer2.classList.add("active1")
    box2__item__fazer1.classList.remove("active1")

})
text__1.addEventListener("click", function () {
    box2__item__fazer2.classList.remove("active1")
    box2__item__fazer1.classList.add("active1")

})