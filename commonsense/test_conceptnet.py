# nuScenes dev-kit.
# Code written by Leilani H. Gilpin, 2019/2020.

import random
import unittest
from typing import Dict, List

import numpy as np
from commonsense.conceptnet import *


class TestConceptnet(unittest.TestCase):
    def test_find_anchor(self):
        """
        Tests the anchor point labeling for the uber example
        and other default "objects"
        """
        concepts = ['ball', 'bicycle', 'trash']
        anchors = ['animal', 'object', 'place', 'plant']
        reason = 'ConceptNet IsA link'
        default_reason = 'Default anchor point'

        for concept in concepts:
            result = make_fact([concept, 'IsA', 'object'], reason)
            trial = find_anchor(concept, anchors)
            self.assertEqual(result, trial)

        # LHG adds spring 2020: test the default anchor
        bad_concepts = ['vehicle', 'mailbox']
        for concept in bad_concepts:
            result = make_fact([concept, 'IsA', 'object'],
                               default_reason)
            trial = find_anchor(concept, anchors)
            self.assertEqual(result, trial)

    def test_make_prolog_fact(self):
        """
        Tests the anchor point labeling for the uber example
        """
        concepts = ['vehicle', 'bicycle']
        anchors = ['animal', 'object', 'place', 'place', 'plant']
        reason = 'ConceptNet IsA link'

        for concept in concepts:
            result = make_prolog_fact([concept, 'IsA', 'object'],
                                      reason)
            trial = ["IsA(" + concept + ", object)", reason]
            self.assertEqual(trial, result)

    def test_make_fact(self):
        """
        Tests the make fact function
        """
        # Tests if the following concepts are recognized as objects with the making of facts
        concepts = ['vehicle', 'bicycle', 'person', 'motorcycle']
        reason = 'ConceptNet IsA link'

        for concept in concepts:
            result = make_fact([concept, 'IsA', 'object'],
                               reason)
            answer = [concept + " IsA object", reason]
            self.assertEqual(answer, result)

    # TODO: Come back and update once Leilani cleaned up function
    def test_clean_phrase(self):
        """
        Tests cleaning out un-necessary words from text
        """
        # Groups of cleaned an uncleaned words in tuples for easy testing
        set_a = ("the cat in hat", "cat_in_hat")
        set_b = ("a car speeding", "car_speeding")
        set_c = ("an elevated sloped road", "elevated_sloped_road")
        set_d = ("and man ran", "man_ran")

        set_list = [set_a, set_b, set_c, set_d]  # Add all sets to a list

        for set in set_list:
            result = clean_phrase(set[0])  # gives cleaned phrase
            answer = set[1]
            self.assertEqual(answer, result)

    def test_clean(self):
        """
        Checks the clean function to make sure that it properly cleans out phrases and leaves strings alone
        """
        set_a = ("man isA object", "man")
        set_b = ("bicycle", "bicycle")
        set_c = ("car isA vehicle", "car")
        set_d = ("car", "car")

        set_list = [set_a, set_b, set_c, set_d]  # Add all sets to a list

        for set in set_list:
            result = clean(set[0])  # gives cleaned phrase
            answer = set[1]
            self.assertEqual(answer, result)

    def test_build_relation(self):
        """
        Checks whether facts are being correctly built
        Answers directly from ConceptNet Website (https://conceptnet.io/)

        """
        # TODO: Not all answers showing up properly from query itself
        # Answers
        a_answer = [['bicycle IsA two_wheel_vehicle', 'ConceptNet'], ['bicycle IsA bicycle', 'ConceptNet'],
                    ['bicycle IsA transportation', 'ConceptNet']]
        b_answer = [['dog IsA loyal_friend', 'ConceptNet'], ['dog IsA pet', 'ConceptNet'],
                    ['dog IsA mammal', 'ConceptNet'], ['dog IsA dog', 'ConceptNet'], ['dog IsA canine', 'ConceptNet']]
        c_answer = [['car CapableOf go_fast', 'ConceptNet'], ['car CapableOf crash', 'ConceptNet'],
                    ['car CapableOf roll_over', 'ConceptNet'], ['car CapableOf slow_down', 'ConceptNet']]
        d_answer = [['vehicle AtLocation street', 'ConceptNet'], ['vehicle AtLocation vehicle', 'ConceptNet']]

        # The prompts with the answers attached
        set_a = (("bicycle", "IsA"), a_answer)
        set_b = (("dog", "IsA"), b_answer)
        set_c = (("car", "CapableOf"), c_answer)
        set_d = (("vehicle", "AtLocation"), d_answer)

        set_list = [set_a, set_b, set_c, set_d]  # Add all sets to a list

        for set in set_list:
            result = build_relation(set[0][0], set[0][1])  # gives cleaned phrase
            answer = set[1]
            self.assertEqual(answer, result)

    def test_aggregate(self):

        a_answer = [['bicycle IsA two_wheel_vehicle', 'ConceptNet'], ['bicycle IsA bicycle', 'ConceptNet'],
                    ['bicycle IsA transportation', 'ConceptNet'], ['bicycle AtLocation garage', 'ConceptNet'],
                    ['bicycle AtLocation street', 'ConceptNet'], ['bicycle AtLocation toy_store', 'ConceptNet']]
        b_answer = [['dog IsA loyal_friend', 'ConceptNet'], ['dog IsA pet', 'ConceptNet'],
                    ['dog IsA mammal', 'ConceptNet'], ['dog IsA dog', 'ConceptNet'], ['dog IsA canine', 'ConceptNet'],
                    ['dog AtLocation kennel', 'ConceptNet'], ['dog AtLocation table', 'ConceptNet'],
                    ['dog CapableOf bark', 'ConceptNet'], ['dog CapableOf guard_your_house', 'ConceptNet'],
                    ['dog CapableOf be_a_pet', 'ConceptNet'], ['dog CapableOf run', 'ConceptNet'],
                    ['dog CapableOf guide_a_blind_person', 'ConceptNet']]
        c_answer = [['car IsA car', 'ConceptNet'], ['car AtLocation city', 'ConceptNet'],
                    ['car AtLocation parking_lot', 'ConceptNet'], ['car AtLocation repair_shop', 'ConceptNet'],
                    ['car AtLocation road', 'ConceptNet'], ['car AtLocation car', 'ConceptNet'],
                    ['car AtLocation freeway', 'ConceptNet'], ['car AtLocation car_show', 'ConceptNet'],
                    ['car CapableOf go_fast', 'ConceptNet'], ['car CapableOf crash', 'ConceptNet'],
                    ['car CapableOf roll_over', 'ConceptNet'], ['car CapableOf slow_down', 'ConceptNet']]
        d_answer = [['vehicle IsA vehicle', 'ConceptNet'], ['vehicle AtLocation street', 'ConceptNet'],
                    ['vehicle AtLocation vehicle', 'ConceptNet'], ['vehicle CapableOf receive_damage', 'ConceptNet']]

        list_of_relations = ["IsA", "AtLocation", "CapableOf"]  # List of relations we will test with

        # The prompts with the answers attached
        set_a = aggregate('bicycle IsA two_wheel_vehicle', list_of_relations)

        set_b = aggregate('dog IsA loyal_friend', list_of_relations)

        set_c = aggregate('car CapableOf go_fast', list_of_relations)

        set_d = aggregate('vehicle AtLocation street', list_of_relations)

        set_list = [set_a, set_b, set_c, set_d]  # Add all sets to a list

        answer_list = [a_answer, b_answer, c_answer, d_answer]  # Adds all answers to a list

        for index in range(len(set_list)):
            self.assertEqual(set_list[index], answer_list[index])

    def test_get_closest_anchor(self):

        concept_a = 'car'
        concept_b = 'dog'
        concept_c = 'human'
        anchors = ['vehicle', 'animal', 'object', 'person']

        # Trying to see if concepts has the isA relation with the above anchors

        self.assertEqual(['car IsA vehicle', 'ConceptNet IsA link'], get_closest_anchor(concept_a, anchors))
        self.assertEqual(['dog IsA animal', 'ConceptNet IsA link'], get_closest_anchor(concept_b, anchors))
        self.assertEqual(['human IsA animal', 'ConceptNet IsA link'], get_closest_anchor(concept_c, anchors))

    def test_check_IsA_relation(self):

        concept = 'car'
        anchors = ['vehicle', 'animal', 'object', 'person']
        for anchor in anchors:
            logging.debug("Searching for an IsA link between %s and %s" % (concept, anchor))

            # Get IsA Relationship edges so all of these edges should return true for IsA
            obj = requests.get(query_prefix + concept + rel_term + 'IsA' + limit_suffix).json()
            edges = obj['edges']

            if edges:
                for edge in edges:
                    if check_IsA_relation(anchor,
                                          edge):  # First call should filter out if works properly and second one should alway return True
                        self.assertEqual(True, check_IsA_relation(anchor, edge))

    def test_clean_concept(self):

        set_a = ("dog", "dog")
        set_b = ("cat-in-the-hat", ["cat", "in", "the", "hat"])
        set_c = ("cat-fight-dog", ["cat", "fight", "dog"])

        set_list = [set_a, set_b, set_c]

        for set in set_list:
            self.assertEqual(set[1], clean_concept(set[0]))

    def test_find_shortest_path(self):

        concept = 'car'
        anchors = ['vehicle', 'animal', 'object', 'person']

        shortest_paths = [['car', 'vehicle'],
                          ['car', 'machine', 'organization', 'animal'],
                          ['car', 'object'],
                          ['car', 'person']]
        for index, anchor in enumerate(anchors):
            self.assertEqual(shortest_paths[index], find_shortest_path(concept, anchor))

    def test_get_shortest_hops(self):

        concepts = ['car', 'dog', 'bicycle']
        answer_set = [('object', ['car', 'object']), ('animal', ['dog', 'animal']), ('object', ['bicycle', 'object'])]

        for index, concept in enumerate(concepts):
            self.assertEqual(answer_set[index], get_shortest_hops(concept))

    def test_clean_search(self):

        test_set = [("a happy dog", "happy_dog"), ("an speeDinG CAR", "speeding_car"), ("smallChange", "smallchange")]

        for test in test_set:
            self.assertEqual(test[1], clean_search(test[0]))

    def test_search_equals(self):

        test_set = [("a happy dog", "happy_dog"), ("an speeDinG CAR", "speeding_car"), ("smallChange", "smallchange"),
                    ("happy dog", "unhappy dog")]

        # All the above should be equal searches except last one

        for index, test in enumerate(test_set):
            if index == 3:
                self.assertEqual(False, search_equals(test[0], test[1]))
            else:
                self.assertEqual(True, search_equals(test[0], test[1]))

    def test_has_any_edge(self):

        # Basically checks whether objects have relation with verbs
        self.assertEqual(True, has_any_edge("car", "drive"))
        self.assertEqual(True, has_any_edge("person", "run"))
        self.assertEqual(False, has_any_edge("car", "eat"))

    def test_has_IsA_edge(self):
        # TODO: for some reason dog is a car and cat is a dog ??
        test_set = [("car", "vehicle", True), ("car", "object", True), ("person", "object", False),
                    ("cat", "animal", True), ("car", "animal", False), ("cat", "vehicle", False),
                    ("bicycle", "object", True), ("dog", "animal", True), ("dog", "car", False), ("cat", "dog", False)]

        for set in test_set:
            self.assertEqual(set[2], has_IsA_edge(set[0], set[1]))

    def test_has_edge(self):

        test_set = [("car", "vehicle", True), ("car", "object", True), ("person", "object", False),
                    ("cat", "animal", True), ("car", "animal", False), ("cat", "vehicle", False),
                    ("bicycle", "object", True), ("dog", "animal", True), ("dog", "car", True), ("cat", "dog", True)]

        for set in test_set:
            self.assertEqual(set[2], has_IsA_edge(set[0], set[1]))

    def test_isA_equals(self):

        test_set = [("dog", "dog in hat", True), ("cat", "cat in the hat", True), ("car", "not contain word", False),
                    ("bicycle", "bicycle isA mode of transport", True), ("motorcycle", "motorbike", False)]

        for set in test_set:
            self.assertEqual(set[2], isA_equals(set[0], set[1]))

    def test_containsConcept(self):

        list_of_facts = [['car IsA vehicle', 'ConceptNet IsA link'],['dog IsA animal', 'ConceptNet IsA link'],['human IsA animal', 'ConceptNet IsA link']]

        concepts = ["car","dog","human"]
        fail_concepts = ["cat","woman","bicycle"]

        for index,fact in enumerate(list_of_facts):
            self.assertEqual(fact[0],containsConcept(concepts[index],list_of_facts))

        for index,fact in enumerate(list_of_facts):
            self.assertEqual(False,containsConcept(fail_concepts[index],list_of_facts))

        #We check both concepts that should pass as well as fail in the testing above

    def test_search_relation(self):

        #This just tests that the function works, not necessarily the accuracy of the function

        a_answer = {'an environmentally friendly mode of trasportation', 'wheeled vehicle', 'a two wheeled method of transportation', 'a vehicle type', 'a two wheel vehicle', 'transportation', 'much smaller than a fire truck', 'steered y handlebars', 'toy', 'bike', 'bicycle', 'mountable transporter device', 'bicycle market category', 'bilaterally symmetric object', 'a two-wheeled vehicle,', 'good exercise', 'a bicycle', 'user powered device', 'a human powered vehicle', 'a vehicle with two wheels', 'an efficient form of human transportation', 'user guided device', 'vehicle'}
        b_answer = {'a nice friend', 'shedding', 'a good friend', 'a faithful companion', 'so big', 'canine', 'a dog', 'mammal', 'pet', 'a domesticated canine', 'happy when it wags its tail', 'domestic animal', 'a canine', 'cuter than your kids', 'an example of a pet', 'a four legged animal', 'dog', 'straining at its leash', 'chap', 'a mans best friend', 'a curious observer of mankind', 'a thing', 'a loyal friend'}
        c_answer = {'drive over a cat', 'carry few persons', 'go fast', 'kill a cat', 'pass another car', 'seat riders', 'crash', 'slow near schools', 'kill a person', 'pull a car', 'rush through traffic', 'corner a corner', 'pass a bus', 'get a flat tire', 'bottom out', 'cost money', 'move quickly', 'travel down the road', 'pass other car', 'serve to transport', 'slow down', 'kill people', 'be heading north', 'move on a road', 'cost a lot of money', 'roll over', 'tail another car', 'set off', 'enter that garage', 'head north', 'need petrol', 'last several years', 'start running', 'roll downhill', "start if it's working", 'fail to start', 'travel over a bridge', 'come up the drive', 'drive up the street', 'back up', 'turn around', 'hit a wall', 'seat people', 'move a person'}
        d_answer = {'vehicle', 'a vehicle', 'a freeway', 'the street'}

        set_a = (("bicycle", "IsA"), a_answer)
        set_b = (("dog", "IsA"), b_answer)
        set_c = (("car", "CapableOf"), c_answer)
        set_d = (("vehicle", "AtLocation"), d_answer)

        answer_list = [a_answer,b_answer,c_answer,d_answer]
        set_list = [set_a,set_b,set_c,set_d]

        for index,answer in enumerate(answer_list):
            self.assertEqual(answer,set(search_relation(set_list[index][0][0],set_list[index][0][1])))

    def test_isConfusion(self):

        answer_set = [("hurricane",True),("storm",True),("earthquake",True),("cat",False),("dog",False),("car",False)]

        for set in answer_set:
            self.assertEqual(set[1],isConfusion(set[0]))

    def test_can_move(self):

        answer_set = [("cat",True),("car",True),("dog",True),("human",True),("trash",False),("apple",False)]

        for set in answer_set:
            self.assertEqual(set[1],can_move(set[0]))

    def test_can_propel(self):

        list_of_contexts_a = ['hurricane', 'sunny', 'storm', 'earthquake','raining']
        list_of_contexts_b = [ 'sunny', 'raining']
        list_of_contexts_c = ['hurricane', 'sunny','raining']

        test_list = [list_of_contexts_a,list_of_contexts_b,list_of_contexts_c]
        answers = [True,False,True]

        for index,list in enumerate(test_list):
            self.assertEqual(answers[index],can_propel(list))


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()
