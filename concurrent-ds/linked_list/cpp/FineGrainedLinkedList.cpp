// program definition for fine-grained linked list
// here linked list is sorted unlike coarse-grained linked list
// 
// 
#include "FineGrainedLinkedList.h"
#include <cstdint>

FineGrainNode::FineGrainNode(int key): m_key(key){}
FineGrainNode::FineGrainNode(int key, FineGrainNode* next): m_key(key), m_next(next){};




// linked list defintion
// for fine-grained keys are sorted

FineGrainLinkedList::FineGrainLinkedList(){
    // initialize sentinle nodes
    m_head = new FineGrainNode(INT64_MIN);
    m_tail = new FineGrainNode(INT64_MAX);
}

FineGrainLinkedList::~FineGrainLinkedList(){
    FineGrainNode *curr, *freed;
    
      curr = m_head;
      while (curr != nullptr) {
        freed = curr;
        curr = curr->m_next;
        delete freed;
      }
}






