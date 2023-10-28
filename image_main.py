from PIL import Image, ImageDraw
import sys

# Helper function to test if there is a pixel at a location
def is_pixel(img, coord):
    try:
        img.getpixel(coord)
        return True
    except IndexError:
        return False


# 1. Function to get dimensions of an image
def get_image_dimensions(image_path):
    """
    Return the dimensions (width, height) of the image.

    Parameters:
    - image_path: str, path to the image.

    Returns:
    - tuple, (width, height)
    """
    # Open the image
    with Image.open(image_path) as img:
        # coord = (x, y)
        # img.getpixel(coord) -> returns: IF THERE IS A PIXEL (R, G, B). IF NOT 'IndexError.'
        x = 0
        y = 0
        coord = (x, y)
        while is_pixel(img, coord):  # first find size in x dimension
            x += 1
            coord = (x, y)
        img_width = x
        x = 0
        coord = (x, y)
        while is_pixel(img, coord):  # find size in y dimension
            y += 1
            coord = (x, y)
        img_height = y

    return (img_width, img_height)  # (width, height)


# 2. Function to get the mean color of the image
def get_mean_color(image_path):
    """
    Return the mean color (mean R, mean G, mean B) of the image.

    Parameters:
    - image_path: str, path to the image.

    Returns:
    - tuple, (mean R, mean G, mean B)
    """
    width, height = get_image_dimensions(image_path)
    with Image.open(image_path) as img:  # Opens the image
        return mean_color_square(img, 0, 0, width, height)  # returns mean RGB of image using full width and height


# mean value of individual section
def mean_color_square(img, x_0, y_0, width, height):
    """
    Return the mean color (mean R, mean G, mean B) of the chosen section of the image.

    Parameters:
    - img: the image
    - x_0, y_0: starting coordinate, included in the square, index value
    - width: width of the square
    - height: height of the square


    Returns:
    - tuple, (mean R, mean G, mean B)
    """
    value_list = []
    # adding all values of RGB for each pixel in selected square into value_list
    for x in range(x_0, x_0 + width):
        for y in range(y_0, y_0 + height):
            rgb_val = img.getpixel((x, y))
            value_list.append(rgb_val)
    # total values of RGB from all pixels in selected square
    red = 0
    green = 0
    blue = 0   
    for value in value_list:
        red += value[0]
        green += value[1]
        blue += value[2]
    # find average RGB values in the selected square
    mean_red = round(red / len(value_list))
    mean_blue = round(blue / len(value_list))
    mean_green = round(green / len(value_list))
    return (mean_red, mean_green, mean_blue)

def image_of_avgs(image_path, num_x, num_y):
    """
    Return an image containing the mean color values in squares of an inputted size
    
    Parameters
    - image_path: str, path to the image
    - num_x: int, num of squares horizonatlly
    - num_y: int, num of squares vertically
    
    
    Returns: Image
    """
    width, height = get_image_dimensions(image_path)
    # Using total width and height and number of small rectangles to find width and height of sections
    mini_width = width // num_x
    mini_height = height // num_y
    square_value_list = []  # list of average RGB values for each section
    with Image.open(image_path) as img:
        # Finds average color of each section and appends into square_value_list
        for x in range(0, num_x):
            for y in range(0, num_y):
                square_value = mean_color_square(img, x * mini_width, y * mini_height, mini_width, mini_height)
                square_value_list.append(square_value)
    new_image = Image.new('RGB', (width, height))  # Creating new image in RGB spectrum with same width and height of full image
    # Creating rectangles with average RGB values using ImageDraw module
    draw = ImageDraw.Draw(new_image)
    sq_num = 0
    for x in range(0, num_x):
        for y in range(0, num_y):
            start_coord = (x * mini_width, y * mini_height)
            end_coord = ((x + 1) * mini_width, (y + 1) * mini_height)
            draw.rectangle([start_coord, end_coord], fill=(square_value_list[sq_num]))
            sq_num += 1
    return new_image


# Main function to test the above functions
def main():
    if len(sys.argv) < 2:
        print("Usage: python image_main.py <image_path>")
        sys.exit(1)

        # Use the provided image path
    image_path = sys.argv[1]

    # Test get_image_dimensions
    dims = get_image_dimensions(image_path)
    print(f"Image Dimensions: {dims}")

    # Test get_mean_color
    mean_color = get_mean_color(image_path)
    print(f"Mean Color: {mean_color}")

    # Test helper mean_color_square
    # with Image.open(image_path) as img:
    #     test_mean = mean_color_square(img, 0, 0, dims[0], dims[1])
    #     print("Helper Test: ", (test_mean == mean_color) )
    # Github test

    avg_img = image_of_avgs(image_path, 20, 15)
    avg_img.show()


if __name__ == "__main__":
    main()
