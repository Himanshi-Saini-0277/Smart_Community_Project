// Example of adding a simple animation or effect
document.addEventListener('DOMContentLoaded', function() {
    const features = document.querySelectorAll('.feature img');
    features.forEach(feature => {
        feature.addEventListener('mouseover', () => {
            feature.style.transform = 'scale(1.1)';
        });
        feature.addEventListener('mouseout', () => {
            feature.style.transform = 'scale(1)';
        });
    });
});
