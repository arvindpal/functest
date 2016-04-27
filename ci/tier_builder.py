#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import yaml

import tier_handler as th


class TierBuilder:
    def __init__(self, ci_installer, ci_scenario, testcases_file):
        self.ci_installer = ci_installer
        self.ci_scenario = ci_scenario
        self.testcases_file = testcases_file
        self.dic_tier_array = None
        self.tier_objects = []
        self.testcases_yaml = None
        self.generate_tiers()

    def read_test_yaml(self):
        with open(self.testcases_file) as f:
            self.testcases_yaml = yaml.safe_load(f)

        self.dic_tier_array = []
        for tier in self.testcases_yaml.get("tiers"):
            self.dic_tier_array.append(tier)

    def generate_tiers(self):
        if self.dic_tier_array is None:
            self.read_test_yaml()

        del self.tier_objects[:]
        for dic_tier in self.dic_tier_array:
            tier = th.Tier(name=dic_tier['name'],
                           order=dic_tier['order'],
                           ci=dic_tier['ci'],
                           description=dic_tier['description'])

            for dic_testcase in dic_tier['testcases']:
                installer = dic_testcase['dependencies']['installer']
                scenario = dic_testcase['dependencies']['scenario']
                dep = th.Dependency(installer, scenario)

                testcase = th.TestCase(name=dic_testcase['name'],
                                       dependency=dep,
                                       description=dic_testcase['description'])
                if testcase.is_compatible(self.ci_installer, self.ci_scenario):
                    tier.add_test(testcase)

            self.tier_objects.append(tier)

    def __str__(self):
        output = ""
        for i in range(0, len(self.tier_objects)):
            output += str(self.tier_objects[i]) + "\n"
        return output