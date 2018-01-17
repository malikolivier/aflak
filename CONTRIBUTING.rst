============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

Bug reports
===========

When `reporting a bug <https://github.com/malikolivier/aflak/issues>`_ please
include:

    * Your operating system name and version.
    * Any details about your local setup that might be helpful in
      troubleshooting.
    * Detailed steps to reproduce the bug.

Feature requests and feedback
=============================

The best way to send feedback is to file an issue at
https://github.com/malikolivier/aflak/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Code contributions are welcome :)

Development
===========

To set up `aflak` for local development:

1. Fork `aflak <https://github.com/malikolivier/aflak>`_
   (look for the "Fork" button).
2. Clone your fork locally::

    git clone git@github.com:your_name_here/aflak.git

3. Create a branch for local development::

    git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

4. When you're done making changes, run all the checks::

    make pep8
    pytest


5. Commit your changes and push your branch to GitHub::

    git add your-changes
    git commit
    git push origin name-of-your-bugfix-or-feature

6. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

If you need some code review or feedback while you're developing the code just
make the pull request.

For merging, you should:

1. Update documentation when there's new API, functionality etc.
2. Add a note to ``CHANGELOG.rst`` about the changes.
3. Add yourself to ``AUTHORS.rst``.

.. [1] If you don't have all the necessary python package available locally
       you can rely on Travis - it will
       `run the tests <https://travis-ci.org/malikolivier/aflak/pull_requests>`_
       for each change you add in the pull request.

       It will be slower though ...
