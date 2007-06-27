import os
import re

from reviewboard.scmtools.core import SCMTool, ChangeSet, HEAD, PRE_CREATION

class PerforceTool(SCMTool):
    def __init__(self, repository):
        SCMTool.__init__(self, repository)

        import p4
        self.p4 = p4.P4()
        self.p4.port = repository.path
        self.p4.user = repository.username
        self.p4.password = repository.password

        # We defer actually connecting until just before we do some operation
        # that requires an active connection to the perforce depot.  This
        # connection is then left open as long as possible.

        self.uses_atomic_revisions = True

    def __del__(self):
        self._disconnect()

    def _connect(self):
        if not self.p4.connected:
            self.p4.connect()

    def _disconnect(self):
        if self.p4.connected:
            self.p4.disconnect()

    def get_pending_changesets(self, userid):
        self._connect()
        return map(self.get_changeset,
                   [x.split()[1] for x in
                       self.p4.run_changes('-s', 'pending', '-u', userid)])

    def get_changeset(self, changesetid):
        self._connect()
        changeset = self.p4.run_describe('-s', str(changesetid))
        self._disconnect()
        return self.parse_change_desc(changeset, changesetid)

    def get_diffs_use_absolute_paths(self):
        return True

    def get_file(self, path, revision=HEAD):
        if revision == PRE_CREATION:
            return ''

        if revision == HEAD:
            file = path
        else:
            file = '%s#%s' % (path, revision)

        f = os.popen('p4 -p %s -u %s print -q %s' % (self.p4.port,
                                                     self.p4.user, file))
        data = f.read()
        failure = f.close()

        if failure:
            raise Exception('unable to fetch %s from perforce' % file)

        return data

    def parse_diff_revision(self, file_str, revision_str):
        # Perforce has this lovely idiosyncracy that diffs show revision #1 both
        # for pre-creation and when there's an actual revision.
        self._connect()

        filename, revision = revision_str.rsplit('#', 1)
        files = self.p4.run_files(revision_str)

        if len(files) == 0:
            revision = PRE_CREATION

        self._disconnect()

        return filename, revision

    def get_filenames_in_revision(self, revision):
        return self.get_changeset(revision).files

    @staticmethod
    def parse_change_desc(changedesc, changenum):
        changeset = ChangeSet()
        changeset.changenum = changenum

        # At it's most basic, a perforce changeset description has three
        # sections.
        #
        # ---------------------------------------------------------
        # Change <num> by <user>@<client> on <timestamp> *pending*
        #
        #         description...
        #         this can be any number of lines
        #
        # Affected files ...
        #
        # //depot/branch/etc/file.cc#<revision> branch
        # //depot/branch/etc/file.hh#<revision> delete
        # ---------------------------------------------------------
        #
        # At the moment, we only care about the description and the list of
        # files.  We take the first line of the description as the summary.
        #
        # We parse the username out of the first line to check that one user
        # isn't attempting to "claim" another's changelist.  We then split
        # everything around the 'Affected files ...' line, and process the
        # results.
        changeset.username = changedesc[0].split(' ')[3].split('@')[0]

        description = '\n'.join(changedesc[1:])
        file_header = re.search('Affected files ...', description)

        changeset.description = '\n'.join([x.strip() for x in
                description[:file_header.start()].split('\n')]).strip()
        changeset.files = filter(lambda x: len(x),
            [x.strip().split('#', 1)[0] for x in
                description[file_header.end():].split('\n')])

        split = changeset.description.find('\n\n')
        if split >= 0 and split < 100:
            changeset.summary = \
                changeset.description.split('\n\n', 1)[0].replace('\n', ' ')
        else:
            changeset.summary = changeset.description.split('\n', 1)[0]

        return changeset

    def get_fields(self):
        return ['changenum', 'diff_path']
