// console.log("hello world");
new WOW().init();




(function() {
    const links = document.getElementsByTagName('a')
    const currentUrl = location.href
    for (const link of links) {
        if (link.href === currentUrl) {
            link.classList.add('active')
        }
    }
}())