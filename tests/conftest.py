"""pytest configuration file."""

import os

import obsws_python as obsws
from dotenv import find_dotenv, load_dotenv


def pytest_configure(config):
    """Call after command line options are parsed.

    All plugins and initial conftest files are loaded.
    """


def pytest_sessionstart(session):
    """Call after the Session object is created.

    Before performing collection and entering the run test loop.
    """
    # Initialize the OBS WebSocket client
    session.obsws = obsws.ReqClient(
        host=os.environ['OBS_HOST'],
        port=os.environ['OBS_PORT'],
        password=os.environ['OBS_PASSWORD'],
        timeout=5,
    )
    resp = session.obsws.get_version()

    out = (
        'Running tests with:',
        f'OBS Client version: {resp.obs_version} with WebSocket version: {resp.obs_web_socket_version}',
    )
    print(' '.join(out))

    load_dotenv(find_dotenv('.test.env'))

    session.obsws.set_stream_service_settings(
        'rtmp_common',
        {
            'service': 'Twitch',
            'server': 'auto',
            'key': os.environ['OBS_STREAM_KEY'],
        },
    )

    session.obsws.set_current_scene_collection('test-collection')

    session.obsws.create_scene('pytest_scene')
    session.obsws.create_input(
        sceneName='pytest_scene',
        inputName='pytest_input',
        inputKind='color_source_v3',
        inputSettings={
            'color': 3279460728,
            'width': 1920,
            'height': 1080,
            'visible': True,
        },
        sceneItemEnabled=True,
    )
    session.obsws.create_input(
        sceneName='pytest_scene',
        inputName='pytest_input_2',
        inputKind='color_source_v3',
        inputSettings={
            'color': 1789347616,
            'width': 720,
            'height': 480,
            'visible': True,
        },
        sceneItemEnabled=True,
    )
    resp = session.obsws.get_scene_item_list('pytest_scene')
    for item in resp.scene_items:
        if item['sourceName'] == 'pytest_input_2':
            session.obsws.set_scene_item_transform(
                'pytest_scene',
                item['sceneItemId'],
                {
                    'rotation': 0,
                },
            )
            break

    # Create a source filter for the Mic/Aux source
    session.obsws.create_source_filter(
        source_name='Mic/Aux',
        filter_name='pytest filter',
        filter_kind='compressor_filter',
        filter_settings={
            'threshold': -20,
            'ratio': 4,
            'attack_time': 10,
            'release_time': 100,
            'output_gain': -3.6,
            'sidechain_source': None,
        },
    )

    # Create a source filter for the pytest scene
    session.obsws.create_source_filter(
        source_name='pytest_scene',
        filter_name='pytest filter',
        filter_kind='luma_key_filter_v2',
        filter_settings={'luma_max': 0.6509},
    )


def pytest_sessionfinish(session, exitstatus):
    """Call after the whole test run finishes.

    Return the exit status to the system.
    """
    session.obsws.remove_source_filter(
        source_name='Mic/Aux',
        filter_name='pytest filter',
    )

    session.obsws.remove_source_filter(
        source_name='pytest_scene',
        filter_name='pytest filter',
    )

    session.obsws.remove_scene('pytest_scene')

    session.obsws.set_current_scene_collection('default')

    resp = session.obsws.get_stream_status()
    if resp.output_active:
        session.obsws.stop_stream()

    resp = session.obsws.get_record_status()
    if resp.output_active:
        session.obsws.stop_record()

    resp = session.obsws.get_replay_buffer_status()
    if resp.output_active:
        session.obsws.stop_replay_buffer()

    resp = session.obsws.get_studio_mode_enabled()
    if resp.studio_mode_enabled:
        session.obsws.set_studio_mode_enabled(False)

    # Close the OBS WebSocket client connection
    session.obsws.disconnect()


def pytest_unconfigure(config):
    """Call before test process is exited."""
