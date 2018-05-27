from invoke import task


@task
def clean(c):
    print('cleaning dist...')
    c.run('rm -rf dist')


@task
def build(c):
    print('building dist...')
    c.run('python3 setup.py bdist_wheel sdist')


@task
def upload(c):
    print('uploading dist...')
    c.run('twine upload dist/*')
