#
#  SynchronizeController.py
#  IShareCode
#
#  Created by ROGERIO ARAUJO on 05/09/09.
#  Copyright (c) 2009 __MyCompanyName__. All rights reserved.
#

from objc import YES, NO, IBAction, IBOutlet
from Foundation import *
from AppKit import *
from mercurial import hg, bundlerepo
from mercurial import cmdutil

class SynchronizeController(NSWindowController):
	def __new__(cls, directory):
		return cls.alloc().initWithDirectory_(directory)

	def initWithDirectory(self, directory):
		self.directory = directory
		self = self.initWithWindowNibName_owner_("SynchronizeWindow", self)
		self.showWindow_(self)
		self.retain()
		return self
		
	def windowWillClose(self, notification):
		# see comment in self.initWithObject_()
		self.autorelease()
	
	def incoming(self):
		limit = cmdutil.loglimit(opts)
		source, revs, checkout = hg.parseurl(ui.expandpath(source), opts.get('rev'))
		other = hg.repository(cmdutil.remoteui(repo, opts), source)
		ui.status(_('comparing with %s\n') % url.hidepassword(source))
		if revs:
			revs = [other.lookup(rev) for rev in revs]
		common, incoming, rheads = repo.findcommonincoming(other, heads=revs,
                                                       force=opts["force"])
		if not incoming:
			try:
				os.unlink(opts["bundle"])
			except:
				pass
			ui.status(_("no changes found\n"))
			return 1

		cleanup = None
		try:
			fname = opts["bundle"]
			if fname or not other.local():
				# create a bundle (uncompressed if other repo is not local)

				if revs is None and other.capable('changegroupsubset'):
					revs = rheads

				if revs is None:
					cg = other.changegroup(incoming, "incoming")
				else:
					cg = other.changegroupsubset(incoming, revs, 'incoming')
				bundletype = other.local() and "HG10BZ" or "HG10UN"
				fname = cleanup = changegroup.writebundle(cg, fname, bundletype)
				# keep written bundle?
				if opts["bundle"]:
					cleanup = None
				if not other.local():
					# use the created uncompressed bundlerepo
					other = bundlerepo.bundlerepository(ui, repo.root, fname)

			o = other.changelog.nodesbetween(incoming, revs)[0]
			if opts.get('newest_first'):
				o.reverse()
			displayer = cmdutil.show_changeset(ui, other, opts)
			count = 0
			for n in o:
				if count >= limit:
					break
				parents = [p for p in other.changelog.parents(n) if p != nullid]
				if opts.get('no_merges') and len(parents) == 2:
					continue
				count += 1
				displayer.show(other[n])
		finally:
			if hasattr(other, 'close'):
				other.close()
			if cleanup:
				os.unlink(cleanup)

	def postincoming(ui, repo, modheads, optupdate, checkout):
		if modheads == 0:
			return
		if optupdate:
			if (modheads <= 1 or len(repo.branchheads()) == 1) or checkout:
				return hg.update(repo, checkout)
			else:
				ui.status(_("not updating, since new heads added\n"))
		if modheads > 1:
			ui.status(_("(run 'hg heads' to see heads, 'hg merge' to merge)\n"))
		else:
			ui.status(_("(run 'hg update' to get a working copy)\n"))
				
	def pull(self):
		source, revs, checkout = hg.parseurl(ui.expandpath(source), opts.get('rev'))
		other = hg.repository(cmdutil.remoteui(repo, opts), source)
		ui.status(_('pulling from %s\n') % url.hidepassword(source))
		if revs:
			try:
				revs = [other.lookup(rev) for rev in revs]
			except error.CapabilityError:
				err = _("Other repository doesn't support revision lookup, "
						"so a rev cannot be specified.")
				raise util.Abort(err)

		modheads = repo.pull(other, heads=revs, force=opts.get('force'))
		return postincoming(ui, repo, modheads, opts.get('update'), checkout)

	def outgoing(self):
		limit = cmdutil.loglimit(opts)
		dest, revs, checkout = hg.parseurl(
			ui.expandpath(dest or 'default-push', dest or 'default'), opts.get('rev'))
		if revs:
			revs = [repo.lookup(rev) for rev in revs]

		other = hg.repository(cmdutil.remoteui(repo, opts), dest)
		ui.status(_('comparing with %s\n') % url.hidepassword(dest))
		o = repo.findoutgoing(other, force=opts.get('force'))
		if not o:
			ui.status(_("no changes found\n"))
			return 1
		o = repo.changelog.nodesbetween(o, revs)[0]
		if opts.get('newest_first'):
			o.reverse()
		displayer = cmdutil.show_changeset(ui, repo, opts)
		count = 0
		for n in o:
			if count >= limit:
				break
			parents = [p for p in repo.changelog.parents(n) if p != nullid]
			if opts.get('no_merges') and len(parents) == 2:
				continue
			count += 1
			displayer.show(repo[n])

	def push(self):
		dest, revs, checkout = hg.parseurl(
			ui.expandpath(dest or 'default-push', dest or 'default'), opts.get('rev'))
		other = hg.repository(cmdutil.remoteui(repo, opts), dest)
		ui.status(_('pushing to %s\n') % url.hidepassword(dest))
		if revs:
			revs = [repo.lookup(rev) for rev in revs]

		# push subrepos depth-first for coherent ordering
		c = repo['']
		subs = c.substate # only repos that are committed
		for s in sorted(subs):
			c.sub(s).push(opts.get('force'))

		r = repo.push(other, opts.get('force'), revs=revs)

	def email(self):
		print "Email"

	def stop(self):
		print "Stop"

	def configure(self):
		print "Configure"
