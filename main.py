import sys


def validate(data):
    """ validation of input file data """

    try:
        tokens = data.strip().split(",")
        var_count = int(tokens.pop(0))
        operations = list(filter(lambda x: x in ["&", "|", "~", "^"], tokens))
        if len(operations) < len(tokens):
            raise TypeError("Incorrect operation sign")
        if var_count < 0:
            raise TypeError("Var count cannot be negative")
        if var_count == 1 and operations is not ["~"]:
            raise TypeError("1 variable can be only for ~")
        return var_count, operations
    except Exception as e:
        print(f"Error while validating: {e}")


def get_names(count):
    """ generating variable names """

    if count <= 26:
        return [chr(i) for i in range(ord("a"), ord("z") + 1)][:count]
    i = 1
    names = []
    for j in range((count-1)//26 + 1):
        names.extend((chr(x)*i for x in range(ord("a"), ord("z") + 1)))
        i += 1
    return names[:count]


def main():

    try:
        filename = sys.argv[1]
    except:
        print("Specify filename!")
        return

    try:
        with open(filename, "r") as f:
            input_ = f.read()
            var_count, operations = validate(input_)
    except (ValueError, TypeError):
        print("Incorrect file format")
        return
    except (OSError, EOFError):
        print(f"Cannot open the file and read data\n")
        return

    """ map from operator to function """
    apply_operation = {  # dont implement ~ because its unary
        "&": lambda x, y: x & y,
        "|": lambda x, y: x | y,
        "^": lambda x, y: x ^ y,
    }

    try:

        with open(f"table.txt", "w") as f:
            names = get_names(var_count)
            max_name_len = max(map(str.__len__, names))
            spacing = ((max_name_len+1) * " ")
            f.write(spacing.join([*names, *operations]) + "\n")

            for i in range(2**var_count):  # enumerate all binary number representations
                k = 1 << var_count - 1
                cur_bit = 1 if i & k else 0
                results = dict(
                    zip(operations, (cur_bit for _ in range(len(operations))))
                    )
                f.write(f"{cur_bit}{spacing}")

                if "~" in operations:
                    results["~"] = 0 if results["~"] else 1
                k >>= 1

                for j in range(var_count-1):
                    cur_bit = 1 if i & k else 0
                    for operation in operations:
                        if operation != "~":
                            results[operation] = apply_operation[operation](
                                results[operation], cur_bit
                            )
                    k >>= 1
                    f.write(f"{cur_bit}{spacing}")

                f.write(spacing.join(map(str, results.values())) + "\n")

    except (OSError, EOFError):
        print("Cannot save the file")
        return


if __name__ == "__main__":
    if int("".join(map(str, (sys.version_info[i] for i in range(2))))) < 36:
        print(sys.version_info)
        print("You must use Python 3.6 or above")
    else:
        main()