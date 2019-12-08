# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 National Institute of Informatics.
#
# Invenio-Recommender is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Minimal Flask application example.

SPHINX-START

First install Invenio-Recommender, setup the application and load
fixture data by running:

.. code-block:: console

   $ pip install -e .[all]
   $ cd examples
   $ ./app-setup.sh
   $ ./app-fixtures.sh

Next, start the development server:

.. code-block:: console

   $ export FLASK_APP=app.py FLASK_DEBUG=1
   $ flask run

and open the example application in your browser:

.. code-block:: console

    $ open http://127.0.0.1:5000/records/1
    $ open http://127.0.0.1:5000/records/2

To reset the example application run:

.. code-block:: console

    $ ./app-teardown.sh

SPHINX-END
"""

from __future__ import absolute_import, print_function

import os


from flask import Flask, render_template_string
from flask_babelex import Babel
from invenio_theme import InvenioTheme
from flask_menu import register_menu

from invenio_i18n import InvenioI18N
from invenio_assets import InvenioAssets
from invenio_formatter import InvenioFormatter
from invenio_db import InvenioDB, db
from invenio_records import InvenioRecords
from invenio_pidstore import InvenioPIDStore
from invenio_records_ui import InvenioRecordsUI
from invenio_records_ui.views import create_blueprint_from_app


from invenio_recommender import InvenioRecommender
from invenio_recommender.views import blueprint

# Create Flask application
app = Flask(__name__)

InvenioDB(app)
InvenioPIDStore(app)
InvenioRecords(app)

InvenioTheme(app)
InvenioRecordsUI(app)
InvenioI18N(app)
InvenioAssets(app)
InvenioFormatter(app)
InvenioRecommender(app)

app.config.update(
    DEBUG=True,
    SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI',
                                           'sqlite:///app.db'),
    RECORDS_UI_DEFAULT_PERMISSION_FACTORY=None,
    RECORDS_UI_ENDPOINTS = { 
        "recid": {
            "pid_type": "recid",
            "route": "/records/<pid_value>",
            "template": "invenio_recommender/record_detail.html",
        },
    },
#RECORDS_UI_ENDPOINTS = {
#    "recid": {
#        "pid_type": "recid",
#        "route": "/records/<pid_value>",
#        "template": "invenio_recommender/record_detail.html",
#        "view_imp": "invenio_recommender.views.my_view",
#    },
#    "recid_export": {
#        "pid_type": "recid",
#        "route": "/records/<pid_value>/export/<format>",
#        "view_imp": "invenio_records_ui.views.export",
#        "template": "invenio_records_ui/export.html",
#    }
#},
    
#: List of allowed titles in badges.
FORMATTER_BADGES_ALLOWED_TITLES = ['DOI', 'doi'],
#: Mapping of titles.
FORMATTER_BADGES_TITLE_MAPPING = {'doi': 'DOI'},
)

app.register_blueprint(blueprint)

app.register_blueprint(create_blueprint_from_app(app))

rec1_uuid = 'deadbeef-1234-5678-ba11-b100dc0ffee5'
"""First record's UUID. It will be given PID 1."""

rec2_uuid = 'deadbeef-1234-5678-ba11-b100dc0ffee6'
"""First record's UUID. It will be given PID 2."""


@app.cli.group()
def fixtures():
    """Command for working with test data."""


@fixtures.command()
def records():
    """Load test data fixture."""
    import uuid
    from invenio_records.api import Record
    from invenio_pidstore.models import PersistentIdentifier, PIDStatus

    # Record 1 - Live record
    with db.session.begin_nested():
        pid1 = PersistentIdentifier.create(
            'recid', '1', object_type='rec', object_uuid=rec1_uuid,
            status=PIDStatus.REGISTERED)
        Record.create({
            'title': 'A dark hole in our understanding of marine ecosystems and their services : perspectives from the mesopelagic community',
            'authors': [
                { 'name': 'Michael A.St.John1'},
                {'name': 'Angel Borja'}, 
                {'name' : 'Guillem Chust'},
                {'name': 'Michael Heath'}, 
                {'name' : 'Ivo Grigorov'},
                {'name': 'Patrizio Mariani'},
                {'name':'Adrian P. Martin'},
                {'name':'Ricardo S. Santos'},
            ],
            'access': 'open',
            'keywords': ['mesopelagic community','food provision','climate regulation','biodiversity','benefits Risks'],
            'abstract' : 'In the face of increasing anthropogenic pressures acting on the Earth system, urgent actions are needed to guarantee efficient resource management and sustainable development for our growing human population. Our oceans - the largest underexplored component of the Earth system - are potentially home for a large number of new resources, which can directly impact upon food security and the wellbeing of humanity. However, the extraction of the resources fostered by marine ecosystems has repercussions for biodiversity and the oceans ability to sequester green house gases and thereby climate. In the search for new “resources to unlock the economic potential of the global oceans, recent observations have identified a large unexploited biomass of mesopelagic fish living in the deep ocean. This biomass has recently been estimated to be 10 billion metric tonnes, at least 10 times larger than previous estimates. If we are able to exploit this community at sustainable levels without impacting upon biodiversity and compromising the oceans’ ability to sequester carbon, we can produce more food and potentially many new nutraceutical products. However, to meet the needs of present generations without compromising the needs of future generations, we need to guarantee a sustainable exploitation of these resources. To do so requires a holistic assessment of the community and an understanding of the mechanisms controlling this biomass, its role in the preservation of biodiversity and its influence on climate as well as management tools able to weigh the costs and benefits of exploitation of this community.',
        }, id_=rec1_uuid)

        PersistentIdentifier.create(
            'recid', '2', object_type='rec', object_uuid=rec2_uuid,
            status=PIDStatus.REGISTERED)
        Record.create({
            'title': '線虫の寿命制御におけるコレステロールの役割',
            'authors': [
                {'name': '庵原, 亜貴子'},
            ],
            'access': 'open',
            'keywords': ['CERN', 'higgs'],
            'abstract':'コレステロールは、その血中量が死亡率に影響を与えることが知られており、寿命制御因子として注目を集めている。しかし、コレステロールが老化に直接どのような影響を与えるかについては未解明な点が多い。線虫は哺乳類と異なり体内でコレステロールを生合成できないため、培地中のコレステロール濃度を変化させることで、体内コレステロール量が寿命に与える影響を調べることができる。本研究において、申請者は線虫を用いてコレステロールが寿命に与える影響を調べ、コレステロールが食餌制限法の一種である断続的飢餓（IF）による寿命延長に重要な因子であることを見出だした。IF は自由摂食と飢餓を繰り返す食餌制限の方法であり、線虫からマウスに至る様々な動物で老化を遅延させ、寿命を延長させることが知られている。そこで、培地中のコレステロール濃度を増減させ、IF 下の寿命への影響を調べた。その結果、コレステロールを含まない培地で線虫を飼育することで、IF による寿命延長が著しく抑制されることを明らかにした。次に、コレステロールが飢餓による遺伝子の発現変化に及ぼす影響について、マイクロアレイを行い網羅的に調べた。その結果、転写因子DAF-16 のターゲット遺伝子の飢餓による発現誘導に、コレステロールが必要であることを見出だした。更に、コレステロールは飢餓によって引き起こされるDAF-16 の核内移行を制御していることを明らかにした。線虫において、NAP-1 (nucleosome assembly protein-1) がコレステロールと結合し、コレステロール依存的にDAF-16 の転写活性を上昇させることが報告されていた。そこで、NAP-1 がDAF-16 の細胞内局在制御とIF による寿命延長に関与するかどうかを調べた。その結果、nap-1 をノックダウンすることで、コレステロールの欠乏と同様に、飢餓によるDAF-16 の核内移行とIF による寿命延長が抑制された。さらに、コレステロール欠乏下においてnap-1 ノックダウンを行っても、DAF-16 の核内移行とIF による寿命延長に対する更なる抑制効果は見られなかった。これらの結果から、コレステロールは少なくとも部分的にはNAP-1 と同じ経路を介して、DAF-16 の核内移行とIF による寿命延長を制御していることが示唆された。本研究は食餌制限法の一種であるIF による寿命延長においてコレステロールが重要な役割を担っていることを示し、そのコレステロールによる寿命制御メカニズムの一端を解明したものである。'
        }, id_=rec2_uuid)

        # Record 3 - Deleted PID with record
        rec3_uuid = uuid.uuid4()
        pid = PersistentIdentifier.create(
            'recid', '3', object_type='rec', object_uuid=rec3_uuid,
            status=PIDStatus.REGISTERED)
        pid.delete()
        Record.create({'title': 'Live '}, id_=rec3_uuid)

        # Record 4 - Deleted PID without a record
        PersistentIdentifier.create(
            'recid', '4', status=PIDStatus.DELETED)

        # Record 5 - Registered PID without a record
        PersistentIdentifier.create(
            'recid', '5', status=PIDStatus.REGISTERED)

        # Record 6 - Redirected PID
        pid = PersistentIdentifier.create(
            'recid', '6', status=PIDStatus.REGISTERED)
        pid.redirect(pid1)

        # Record 7 - Redirected non existing endpoint
        doi = PersistentIdentifier.create(
            'doi', '10.1234/foo', status=PIDStatus.REGISTERED)
        pid = PersistentIdentifier.create(
            'recid', '7', status=PIDStatus.REGISTERED)
        pid.redirect(doi)

        # Record 8 - Unregistered PID
        PersistentIdentifier.create(
            'recid', '8', status=PIDStatus.RESERVED)

    db.session.commit()
