# GluonCv Semantic Segmentation  Data Augmentation

### Definitions :

- **Base_size:** base_size is only used when resizing the image (for example, when augmenting, one possibility would be to resize the image anywhere between 0.5xbase_size and 2xbase_size)
- **Crop_size:** called crop_size when augmenting the data, it's actually the final crop size of the image before it's passed to the network

### Augmentation Process :

When augmenting your data using our custom data-augmentation function , multiple things might happen:

 **1-**  First possibility :

- The image might be flipped left or right.
- The image is resized anywhere between 0.5xbase_size and 2xbase_size.
- If the width or height of the image are lower than the crop_size, black padding is added.
- The image is then cropped anywhere to match the crop_size.
- Blur might be added to the image.

**2-** Second Possibility:

- The image might be resized to crop_size x crop_size and returned to the training network.

**3-** Third Possibility:

- If the height or width of the image are lower than the crop_size,black padding is added.
- The image is cropped to match crop_size, it's cropped either by using :
  - x=0 , y=0
  - x=width-crop_size, y=0
  - x=0, y=height-crop_size
  - x=width-crop_size, height-crop_size
- Blur might be added to the image.

**4- ** Fourth Possibility:

- If data_augmentation is false , the image is resized to crop_size x crop_size.