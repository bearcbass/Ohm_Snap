
const handleImageScale = (image: HTMLImageElement) => {
    const LONG_SIDE_LENGTH = 1024
    let w = image.naturalWidth;
    let h = image.naturalHeight;
    return {height: h, width: w};
}

export { handleImageScale };