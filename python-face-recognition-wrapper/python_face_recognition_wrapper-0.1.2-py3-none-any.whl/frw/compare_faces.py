import argparse
import face_recognition


parser = argparse.ArgumentParser()


parser.add_argument(
    '--known_image', '-ki', type=str,
    help="path of known image"
)
parser.add_argument(
    '--unknown_image', '-uki', type=str,
    help="path of unknown image"
)
parser.add_argument(
    '--output', '-o', type=str,
    help="path to write results"
)


class FaceCompare:
    def __init__(
        self,
        known_image_path=None,
        unknown_image_path=None,
        result_file_path=None
    ):
        self.known_image_path = known_image_path
        self.unknown_image_path = unknown_image_path
        self.results = None
        self.result_file_path = result_file_path

    def get_compare_result(self):
        known_image = face_recognition.load_image_file(self.known_image_path)
        unknown_image = face_recognition.load_image_file(self.unknown_image_path)

        known_encoding = face_recognition.face_encodings(known_image)
        unknown_encoding = face_recognition.face_encodings(unknown_image)
        if unknown_encoding:
            uki1 = unknown_encoding[0]
        else:
            return

        self.results = face_recognition.compare_faces(
            known_encoding, uki1)

        return self.results

    def save(self):
        if self.results is None:
            self.get_compare_result()

        with open(self.result_file_path, "w") as _file:
            if self.results is None:
                _file.write('False\r\n')
            else:
                for _ in self.results:
                    _file.write(str(_) + '\r\n')


if __name__ == "__main__":
    args = parser.parse_args()

    output = args.output

    kw = dict(
        known_image_path=args.known_image,
        unknown_image_path=args.unknown_image
    )

    if output:
        kw['result_file_path'] = output
        FaceCompare(**kw).save()
    else:
        print(FaceCompare(**kw).get_compare_result())
