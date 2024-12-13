from setuptools import setup, Extension


def main():
    setup(
        name="custom_json",
        version="1.0.0",
        author="Evgeniy Saluev",
        ext_modules=[
            Extension(
                'custom_json',
                ['.10/custom_json.c']
            )
        ]
    )


if __name__ == "__main__":
    main()
