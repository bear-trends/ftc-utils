from .importer import Importer
from .exporter import Exporter


def load_importer_exporter(
    mode='local',
    aws_bucket='',
    local_path=''
):
    """Make importer and exporter classes

    Args:
        mode (str, optional): exporting mode, s3 or local.
            Defaults to 'local'.
        aws_bucket (str, optional): if mode = 's3'.
            Defaults to ''.
        local_path (str, optional): if mode = 'local'.
            Defaults to ''.

    Returns:
        [utils.Importer]: Importer module
        [utils.Exporter]: Exporter module
    """
    importer = Importer(
        mode=mode,
        aws_bucket=aws_bucket,
        local_path=local_path
    )

    exporter = Exporter(
        mode=mode,
        aws_bucket=aws_bucket,
        local_path=local_path
    )

    return importer, exporter
