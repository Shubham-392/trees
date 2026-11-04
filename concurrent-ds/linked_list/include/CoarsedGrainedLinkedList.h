 /*
  * Coarse-Grained Synchronization:
  * take a sequential implementation of the class, add a scalable lock field, and ensure
  * that each method call acquires and releases that lock. We call this approach
  * coarse-grained synchronization.
  * 
  * 
  */
#pragma once
#include "UnSyncLinkedList.h"
#include <mutex>



class CoarseGrainedLinkedList: public UnSyncLinkedList{
    public:
        CoarseGrainedLinkedList() = default;
        CoarseGrainedLinkedList(const std::vector<int>& arr);
        ~CoarseGrainedLinkedList() = default;
        // public members
        void add(int key) override; // gives out exception for duplicate key insertion
        void remove(int key) override;
        void display() override;
        int getSize() override;

        LinkedListNode* getHead();
        LinkedListNode* getTail();
        
    private:
        // mutex
        std::mutex mux_;
        
};