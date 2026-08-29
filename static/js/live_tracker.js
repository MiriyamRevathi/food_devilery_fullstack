/**
 * Simulated Live Map Tracking & Marker Pin Animation Module
 */

function animateDeliveryMarker(markerId, pathCoords) {
    const marker = document.getElementById(markerId);
    if (!marker || !pathCoords || pathCoords.length < 2) return;

    let step = 0;
    const interval = setInterval(() => {
        if (step >= pathCoords.length) {
            clearInterval(interval);
            return;
        }
        const point = pathCoords[step];
        marker.style.left = point.x + '%';
        marker.style.top = point.y + '%';
        step++;
    }, 1500);
}
