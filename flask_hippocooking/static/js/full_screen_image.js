 // Open image in fullscreen modal
 function openFullScreen(anchor) {
    const imageSrc = anchor.href;
    const modal = document.createElement('div');
    modal.style.position = 'fixed';
    modal.style.top = '0';
    modal.style.left = '0';
    modal.style.width = '100vw';
    modal.style.height = '100vh';
    modal.style.backgroundColor = 'rgba(0, 0, 0, 0.9)';
    modal.style.display = 'flex';
    modal.style.justifyContent = 'center';
    modal.style.alignItems = 'center';
    modal.style.zIndex = '1000';

    const img = document.createElement('img');
    img.src = imageSrc;
    img.style.maxWidth = '100%';
    img.style.maxHeight = '100%';
    img.alt = anchor.querySelector('img').alt;

    // Close modal on click
    modal.addEventListener('click', () => {
        modal.remove();
    });

    modal.appendChild(img);
    document.body.appendChild(modal);
}