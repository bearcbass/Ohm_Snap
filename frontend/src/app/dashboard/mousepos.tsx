import { useEffect, useRef } from 'react';

interface MousePositionComponentProps {
  imageSrc: string|null;
  setCoords: (x: number, y: number) => void
}

const MousePositionComponent: React.FC<MousePositionComponentProps> = ({imageSrc, setCoords}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const context = canvas?.getContext('2d');
    context!.clearRect(0, 0, canvas!.width, canvas!.height);

    const image = new Image();
    image.src = imageSrc ? imageSrc : ""; // Adjust the path


    const drawCircle = (cx: number, cy: number, radius: number) => {
      context!.beginPath();
      context!.arc(cx, cy, radius, 0, 2 * Math.PI);
      context!.fill(); // Fill the circle with color
      context!.closePath();
    };
    image.onload = () => {
      const picturePosition = { x: 0, y: 0 }; // Adjust according to your layout
      canvas?.addEventListener('click', (event) => {
        const mousePosition = {
          x: event.clientX - canvas.getBoundingClientRect().left,
          y: event.clientY - canvas.getBoundingClientRect().top,
        };
        const relativeX = mousePosition.x - picturePosition.x;
        const relativeY = mousePosition.y - picturePosition.y;
        if (relativeX * relativeY > 0) {
          console.log(`Mouse Position: (${mousePosition.x}, ${mousePosition.y})`);
          console.log(`Relative Position: (${relativeX}, ${relativeY})`);
          context!.clearRect(0, 0, canvas!.width, canvas!.height);
          context?.drawImage(image, 0, 0);
          drawCircle(relativeX, relativeY, 10)
          setCoords(relativeX, relativeY)
        }
      })
      context?.drawImage(image, 0, 0);
      // Draw the image on the canvas
    };
  }, [imageSrc]);

  return <canvas ref={canvasRef} width={800} height={600} />;
};

export default MousePositionComponent;


