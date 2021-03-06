# Copyright 2008 Red Hat, Inc. and/or its affiliates.
#
# Licensed to you under the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.  See the files README and
# LICENSE_GPL_v2 which accompany this distribution.
#

SUBDIRS = storage

dist_vdsm_DATA = \
	betterThreading.py \
	caps.py \
	clientIF.py \
	configNetwork.py \
	config.py \
	define.py \
	dsaversion.py \
	guestIF.py \
	hooking.py \
	hooks.py \
	kaxmlrpclib.py \
	ksm.py \
	libvirtconnection.py \
	libvirtev.py \
	libvirtvm.py \
	logUtils.py \
	neterrors.py \
	netinfo.py \
	pthread.py \
	SecureXMLRPCServer.py \
	supervdsm.py \
	supervdsmServer.py \
	utils.py \
	vdsmDebugPlugin.py \
	vm.py

nodist_vdsm_DATA = \
	constants.py

nodist_vdsm_SCRIPTS = \
	vdsm-restore-net-config \
	vdsm-store-net-config

nodist_noinst_DATA = \
	logger.conf \
	sudoers.vdsm \
	vdsm.conf.sample \
	vdsmd \
	vdsm-sosplugin.py

dist_vdsm_SCRIPTS = \
	addNetwork \
	delNetwork \
	get-conf-item \
	get-vm-pid \
	mk_sysprep_floppy \
	prepare-vmchannel \
	respawn \
	set-conf-item \
	vdsm \
	write-net-config

dist_man8_MANS = \
	vdsmd.8

vdsm_SUBST = \
	$(nodist_vdsm_DATA) \
	$(nodist_vdsm_SCRIPTS) \
	$(nodist_noinst_DATA)

CLEANFILES = \
	$(vdsm_SUBST)

EXTRA_DIST = \
	logger.conf.in \
	mk-vdsm-conf-sample.py \
	vdsmd.in \
	vdsm-libvirt-logrotate \
	vdsm-logrotate \
	vdsm-logrotate.conf \
	vdsm-restore-net-config.in \
	vdsm.rwtab \
	vdsm-sosplugin.py.in \
	vdsm-store-net-config.in

# Reference:
# http://www.gnu.org/software/automake/manual/html_node/Scripts.html
do_subst = sed -e "s,[@]CONFDIR[@],$(vdsmconfdir),g" \
	    -e "s,[@]VDSMLOGDIR[@],$(vdsmlogdir),g" \
	    -e "s,[@]VDSMDIR[@],$(vdsmdir),g" \
	    -e "s,[@]HOOKSDIR[@],$(vdsmhooksdir),g" \
	    -e "s,[@]VDSMRUNDIR[@],$(vdsmrundir),g" \
	    -e "s,[@]VDSMLIBDIR[@],$(vdsmlibdir),g" \
	    -e "s,[@]POOLSDIR[@],$(vdsmpoolsdir),g" \
	    -e "s,[@]BACKUPDIR[@],$(vdsmbackupdir),g" \
	    -e "s,[@]LIBEXECDIR[@],$(vdsmexecdir),g" \
	    -e "s,[@]TRUSTSTORE[@],$(vdsmtsdir),g"

$(vdsm_SUBST): Makefile
	if test "$@" = "vdsm.conf.sample"; then \
		python $(srcdir)/mk-vdsm-conf-sample.py \
			$(srcdir)/config.py > vdsm.conf.sample; \
	elif test -f "$@.in"; then \
		$(do_subst) < $@.in > $@; \
	else \
		$(do_subst) < $(srcdir)/$@.in > $@; \
	fi

install-data-hook:
	chmod 440 $(DESTDIR)$(sysconfdir)/sudoers.d/50_vdsm
	chmod 775 $(DESTDIR)$(localstatedir)/lib/libvirt/qemu/channels

install-data-local: install-data-init install-data-logger \
		install-data-rwtab install-data-logrotate \
		install-data-sudoers install-data-sosplugin
	$(MKDIR_P) $(DESTDIR)$(vdsmtsdir)/keys
	$(MKDIR_P) $(DESTDIR)$(vdsmtsdir)/certs
	$(MKDIR_P) $(DESTDIR)$(vdsmlogdir)
	$(MKDIR_P) $(DESTDIR)$(vdsmrundir)
	$(MKDIR_P) $(DESTDIR)$(vdsmlibdir)/netconfback
	$(MKDIR_P) $(DESTDIR)$(vdsmpoolsdir)
	$(MKDIR_P) $(DESTDIR)$(vdsmbackupdir)
	$(MKDIR_P) $(DESTDIR)$(localstatedir)/lib/libvirt/qemu/channels

uninstall-local: uninstall-data-init uninstall-data-logger \
		uninstall-data-rwtab uninstall-data-logrotate \
		uninstall-data-sudoers uninstall-data-sosplugin

install-data-init:
	$(MKDIR_P) $(DESTDIR)$(sysconfdir)/rc.d/init.d
	$(INSTALL_SCRIPT) vdsmd $(DESTDIR)$(sysconfdir)/rc.d/init.d/vdsmd

uninstall-data-init:
	$(RM) $(DESTDIR)$(sysconfdir)/rc.d/init.d/vdsmd

install-data-logger:
	$(MKDIR_P) $(DESTDIR)$(vdsmconfdir)
	$(INSTALL_DATA) logger.conf $(DESTDIR)$(vdsmconfdir)/logger.conf

uninstall-data-logger:
	$(RM) $(DESTDIR)$(vdsmconfdir)/logger.conf

install-data-rwtab:
	$(MKDIR_P) $(DESTDIR)$(sysconfdir)/rwtab.d
	$(INSTALL_DATA) $(srcdir)/vdsm.rwtab \
		$(DESTDIR)$(sysconfdir)/rwtab.d/vdsm

uninstall-data-rwtab:
	$(RM) $(DESTDIR)$(sysconfdir)/rwtab.d/vdsm

install-data-logrotate:
	$(MKDIR_P) $(DESTDIR)$(sysconfdir)/logrotate.d
	$(INSTALL_DATA) $(srcdir)/vdsm-logrotate.conf \
		$(DESTDIR)$(sysconfdir)/logrotate.d/vdsm
	$(MKDIR_P) $(DESTDIR)$(sysconfdir)/cron.hourly
	$(INSTALL_SCRIPT) $(srcdir)/vdsm-logrotate \
		$(DESTDIR)$(sysconfdir)/cron.hourly/vdsm-logrotate
	$(MKDIR_P) $(DESTDIR)$(sysconfdir)/cron.d
	$(INSTALL_SCRIPT) $(srcdir)/vdsm-libvirt-logrotate \
		$(DESTDIR)$(sysconfdir)/cron.d/vdsm-libvirt-logrotate

uninstall-data-logrotate:
	$(RM) $(DESTDIR)$(sysconfdir)/logrotate.d/vdsm
	$(RM) $(DESTDIR)$(sysconfdir)/cron.hourly/vdsm-logrotate
	$(RM) $(DESTDIR)$(sysconfdir)/cron.d/vdsm-libvirt-logrotate

install-data-sudoers:
	$(MKDIR_P) $(DESTDIR)$(sysconfdir)/sudoers.d
	$(INSTALL_DATA) sudoers.vdsm \
		$(DESTDIR)$(sysconfdir)/sudoers.d/50_vdsm

uninstall-data-sudoers:
	$(RM) $(DESTDIR)$(sysconfdir)/sudoers.d/50_vdsm

install-data-sosplugin:
	$(MKDIR_P) $(DESTDIR)$(pythondir)/sos/plugins
	$(INSTALL_DATA) vdsm-sosplugin.py \
		$(DESTDIR)$(pythondir)/sos/plugins/vdsm.py

uninstall-data-sosplugin:
	$(RM) $(DESTDIR)$(pythondir)/sos/plugins/vdsm.py
