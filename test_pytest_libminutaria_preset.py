import pytest
import os
from datetime import datetime, timedelta
from libminutaria import Timer, Preset
import json

@pytest.fixture
def preset_fixture():
    test_preset = Preset('preset_test', 1, 2, 3, 'preset_test.json')
    yield test_preset
    # Remove the JSON preset test file after the test
    os.remove(test_preset._preset_file)

def test_add(preset_fixture):
    # Add the test preset to preset_test.json
    preset_fixture.add()
    is_preset_written_in_the_file = False
    # Load all data from the file to check if it was effectively written
    with open(preset_fixture._preset_file, 'r') as preset_file_read:
        # Load json presets to be modified
        json_data = json.load(preset_file_read)
        for preset in json_data:
            # Search if the preset does exist
            if preset["name"] == preset_fixture._name:
                is_preset_written_in_the_file = True
    assert(is_preset_written_in_the_file)

def test_add_if_already_exist(preset_fixture):
    preset_fixture.add()
    # Try to add again the same preset to raise an error
    with pytest.raises(ValueError):
        preset_fixture.add()

def test_get(preset_fixture):
    # Add the test preset to preset_test.json
    preset_fixture.add()
    # Check if it was found by checking the returned value
    assert(preset_fixture.get() == {"hours": 1, "minutes": 2, "seconds": 3})

def test_get_if_not_exist(preset_fixture):
    # Change name and check if it raise an error because not found
    with pytest.raises(ValueError):
        preset_fixture.get()

def test_delete(preset_fixture):
    # Add the test preset to preset_test.json
    preset_fixture.add()
    # Check if it was deleted by checking the return value
    assert(preset_fixture.delete())

def test_delete_if_not_exist(preset_fixture):
    # Try to delete it again, it shall raise an error
    with pytest.raises(ValueError):
        preset_fixture.delete()

def test_rename(preset_fixture):
    # Add the test preset to preset_test.json
    preset_fixture.add()
    # Check if it was renamed by checking the return value
    assert(preset_fixture.rename('renamed_preset_test'))
    # Check the same with the Preset.get() method
    preset_fixture._name = 'renamed_preset_test'
    assert(preset_fixture.get())

def test_rename_if_not_exist(preset_fixture):
    # Try to rename a non existing preset in the file
    preset_fixture._name = 'not_existing_preset_test'
    with pytest.raises(ValueError):
        preset_fixture.rename('renamed_preset_test')

def test_rename_if_new_name_is_already_taken(preset_fixture):
    # Add the test preset to preset_test.json
    preset_fixture.add()
    preset_fixture._name = 'existing_preset_test'
    preset_fixture.add()
    with pytest.raises(ValueError):
        preset_fixture.rename('existing_preset_test')

def test_set_duration(preset_fixture):
    # Add the test preset to preset_test.json
    preset_fixture.add()
    # Check if duration was modified by checking the return value
    assert(preset_fixture.set_duration(2, 3, 4))
    # Check if duration was modified by checking the preset's duration
    assert(preset_fixture.get() == {"hours": 2, "minutes": 3, "seconds": 4})

def test_set_duration_if_not_exist(preset_fixture):
    # Try to change duration of a non existing preset
    # Shall raise an error
    with pytest.raises(ValueError):
        preset_fixture.set_duration(2, 3, 4)
