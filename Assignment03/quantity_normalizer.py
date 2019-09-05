"""
This script contains :class: `QuantityNormalizer` which normalizes given
numbers (upto 9999) and quantities by converting given number form into
it's word form, and by expanding the units of the quanity for those defined
in the unit-abbrieviation mapping. The quantity returned is taken care to be
mapped to it's corresponding singular or plural form.

Author:
-------
Aashish Yadavally
"""

import pynini


def normalize(string):
    """
    Uses :func: `normalize_quantities` to normalize the given string

    Input:
    ------
        string (String):
            Input string which is to be word-normalized

    Returns:
    --------
        (String):
            Word-normalized quantity for the corresponding input string
    """
    q_n = QuantityNormalizer()
    return q_n.normalize(string)


class QuantityNormalizer:
    """
    Normalizes given numbers (upto 9999) and quantities by converting given
    number form into it's word form, and by expanding the units of the quanity
    for those defined in the unit-abbrieviation mapping. The quantity returned
    is taken care to be mapped to it's corresponding singular or plural form.

    Here are a few examples:
        - 3 c.      ->  three cups
        - 40 mi.    ->  forty miles
        - 1 lb.     ->  one pound
        - 1000 lbs. ->  thousand pounds

    """
    def __init__(self):
        """
        Initializes :class: QuantityNormalizer with unit, tenth, hundredth,
        thousandth digit mappings; quantity mappings; plural-to-singular
        mappings.

        """
        self.zero_del = pynini.transducer("0", "")

        self.ones_map = pynini.union(
            pynini.transducer("1", "one "),
            pynini.transducer("2", "two "),
            pynini.transducer("3", "three "),
            pynini.transducer("4", "four "),
            pynini.transducer("5", "five "),
            pynini.transducer("6", "six "),
            pynini.transducer("7", "seven "),
            pynini.transducer("8", "eight "),
            pynini.transducer("9", "nine ")
        )

        self.teens_map = pynini.union(
            pynini.transducer("10", "ten"),
            pynini.transducer("11", "eleven "),
            pynini.transducer("12", "twelve "),
            pynini.transducer("13", "thirteen "),
            pynini.transducer("14", "fourteen "),
            pynini.transducer("15", "fifteen "),
            pynini.transducer("16", "sixteen "),
            pynini.transducer("17", "seventeen "),
            pynini.transducer("18", "eighteen "),
            pynini.transducer("19", "nineteen ")
        )

        self.tens_map = pynini.union(
            pynini.transducer("2", "twenty "),
            pynini.transducer("3", "thirty "),
            pynini.transducer("4", "forty "),
            pynini.transducer("5", "fifty "),
            pynini.transducer("6", "sixty "),
            pynini.transducer("7", "seventy "),
            pynini.transducer("8", "eighty "),
            pynini.transducer("9", "ninety ")
        )

        self.hundreds_map = pynini.union(
            pynini.transducer("1", "one hundred "),
            pynini.transducer("2", "two hundred "),
            pynini.transducer("3", "three hundred "),
            pynini.transducer("4", "four hundred "),
            pynini.transducer("5", "five hundred "),
            pynini.transducer("6", "six hundred "),
            pynini.transducer("7", "seven hundred "),
            pynini.transducer("8", "eight hundred "),
            pynini.transducer("9", "nine hundred ")
        )

        self.thousands_map = pynini.union(
            pynini.transducer("1", "one thousand "),
            pynini.transducer("2", "two thousand "),
            pynini.transducer("3", "three thousand "),
            pynini.transducer("4", "four thousand "),
            pynini.transducer("5", "five thousand "),
            pynini.transducer("6", "six thousand "),
            pynini.transducer("7", "seven thousand "),
            pynini.transducer("8", "eight thousand "),
            pynini.transducer("9", "nine thousand ")
        )

        self.units_map = pynini.union(
            pynini.transducer("c.", "cups"),
            pynini.transducer("bbl.", "barrels"),
            pynini.transducer("cm", "centimeters"),
            pynini.transducer("cu.", "cubic"),
            pynini.transducer("GB", "gigabytes"),
            pynini.transducer("doz.", "dozens"),
            pynini.transducer("fl. oz.", "fluid ounces"),
            pynini.transducer("g.", "grams"),
            pynini.transducer("ft.", "feet"),
            pynini.transducer("ha", "hectacres"),
            pynini.transducer("gal.", "gallons"),
            pynini.transducer("KB", "kilobytes"),
            pynini.transducer("in.", "inches"),
            pynini.transducer("kt.", "knots"),
            pynini.transducer("kl.", "kiloliters"),
            pynini.transducer("lb.", "pounds"),
            pynini.transducer("km", "kilometers"),
            pynini.transducer("mi.", "miles"),
            pynini.transducer("l", "liters"),
            pynini.transducer("mph", "miles per hour"),
            pynini.transducer("m", "meters"),
            pynini.transducer("oz.", "ounces"),
            pynini.transducer("MB", "megabytes"),
            pynini.transducer("qt.", "quarts"),
            pynini.transducer("mg", "milligrams"),
            pynini.transducer("rpm", "revolutions per minute"),
            pynini.transducer("ml", "milliliters"),
            pynini.transducer("tbsp.", "tablespoons"),
            pynini.transducer("mm", "millimeters"),
            pynini.transducer("tsp.", "teaspoons"),
            pynini.transducer("W", "watts"),
            pynini.transducer("yd.", "yards"),
            pynini.transducer("kW", "kilowatts"),
            pynini.transducer("B", "bytes"),
            pynini.transducer("kWh", "kilowatts-hour"),
            pynini.transducer("cc", "cubic centimeters")
        )

        self.singularize_map = pynini.union(
            pynini.transducer("cups", "cup"),
            pynini.transducer("barrels", "barrel"),
            pynini.transducer("centimeters", "centimeter"),
            pynini.transducer("gigabytes", "gigabyte"),
            pynini.transducer("dozens", "dozen"),
            pynini.transducer("fluid ounces", "fluid ounce"),
            pynini.transducer("grams", "gram"),
            pynini.transducer("feet", "foot"),
            pynini.transducer("hectacres", "hectacre"),
            pynini.transducer("gallons", "gallon"),
            pynini.transducer("kilobytes", "kilobyte"),
            pynini.transducer("inches", "inch"),
            pynini.transducer("knots", "knot"),
            pynini.transducer("kiloliters", "kiloliter"),
            pynini.transducer("pounds", "pound"),
            pynini.transducer("kilometers", "kilometer"),
            pynini.transducer("miles", "mile"),
            pynini.transducer("liters", "liter"),
            pynini.transducer("miles per hour", "mile per hour"),
            pynini.transducer("meters", "meter"),
            pynini.transducer("ounces", "ounce"),
            pynini.transducer("megabytes", "megabyte"),
            pynini.transducer("quarts", "quart"),
            pynini.transducer("milligrams", "milligram"),
            pynini.transducer("revolutions per minute", "revolution per minute"),
            pynini.transducer("milliliters", "milliliter"),
            pynini.transducer("tablespoons", "tablespoon"),
            pynini.transducer("millimeters", "millimeter"),
            pynini.transducer("teaspoons", "teaspoon"),
            pynini.transducer("watts", "watt"),
            pynini.transducer("yards", "yard"),
            pynini.transducer("kilowatts", "kilowatt"),
            pynini.transducer("bytes", "byte"),
            pynini.transducer("kilowatts-hour", "kilowatt-hour"),
            pynini.transducer("cubic centimeters", "cubic centimeter")
        )



        chars = [chr(i) for i in range(1, 91)] + [r"\[", r"\\", r"\]"] + [chr(i) for i in range(94, 256)]
        self.sigma_star = pynini.union(*chars).closure()
        self.digits = pynini.union("1", "2", "3", "4", "5", "6", "7", "8", "9", "0")
        self.double_digits = pynini.concat(self.digits, self.digits)
        self.triple_digits = pynini.concat(self.double_digits, self.digits)


    def normalize_quantities(self):
        """
        Normalizes quantities based on mappings and left-right context

        Returns:
        --------
            (pynini.fst.vector):
                Word-normalized quantities
        """
        return (
            pynini.cdrewrite(self.units_map, "", "", self.sigma_star, direction="ltr") *
            pynini.cdrewrite(self.singularize_map, "1 ", "", self.sigma_star, direction="ltr") *
            pynini.cdrewrite(self.thousands_map, "", self.triple_digits, self.sigma_star, direction="ltr") *
            pynini.cdrewrite(self.hundreds_map, "", self.double_digits, self.sigma_star, direction="ltr") *
            pynini.cdrewrite(self.tens_map, "", self.digits, self.sigma_star, direction="ltr") *
            pynini.cdrewrite(self.teens_map, "", "", self.sigma_star, direction="ltr") *
            pynini.cdrewrite(self.ones_map, "", "", self.sigma_star, direction="ltr") *
            pynini.cdrewrite(self.zero_del, "", "", self.sigma_star, direction="ltr")
        )


    def normalize(self, string):
        """
        Uses :func: `normalize_quantities` to normalize the given string

        Input:
        ------
            string (String):
                Input string which is to be word-normalized

        Returns:
        --------
            (String):
                Word-normalized quantity for the corresponding input string
        """
        return pynini.compose(string.strip(), self.normalize_quantities()).stringify()
