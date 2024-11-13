document.addEventListener('DOMContentLoaded', () => {
    const lazyImages = document.querySelectorAll('.lazy-image');  // Select all images with the 'lazy-image' class

    const lazyLoadImage = (image) => {
        const src = image.getAttribute('data-src');
        if (src) {
            // console.log('Loading image:', src);  // Log the image URL being loaded
            image.src = src;                    // Set the src attribute to the actual image URL
            image.removeAttribute('data-src');  // Remove the data-src attribute
        }
    };

    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // console.log('Image in view:', entry.target);  // Log when an image enters the viewport
                lazyLoadImage(entry.target);   // Load the image when it enters the viewport
                observer.unobserve(entry.target);  // Stop observing after it’s loaded
            }
        });
    });

    lazyImages.forEach(image => {
        imageObserver.observe(image);  // Observe each image for lazy loading
    });
});
