// Cypress end-to-end tests for the Worldcup app

describe('Worldcup App E2E Tests', () => {
  beforeEach(() => {
    // Serve the index.html locally or use baseUrl in cypress.json
    cy.visit('/index.html');
    // Clear storage before each test
    cy.clearLocalStorage();
  });

  it('Default state: NEW tab and 4 selected', () => {
    cy.get('#listSelector .btn-select.selected').should('have.attr', 'data-list', 'new');
    cy.get('#sizeSelector .btn-select.selected').should('have.attr', 'data-size', '4');
    cy.get('#itemCountInfo').should('contain', '0/4 항목 추가됨 (NEW)');
  });

  it('Add items and enable Start button, then run tournament', () => {
    // Add 4 items
    for (let i = 1; i <= 4; i++) {
      cy.get('#singleInput').type(`Item${i}{enter}`);
    }
    // Start button enabled
    cy.get('#startBtn').should('not.be.disabled').click();
    // Simulate choice flow: click left option until finish
    function pickAll() {
      cy.get('#optA').click();
      cy.get('#optB').then($btn => {
        if ($btn.is(':visible')) pickAll();
      });
    }
    pickAll();
    // Expect modal shown
    cy.get('#modalOverlay.show').should('be.visible');
  });

  it('Save history and display up to 10 entries', () => {
    // Prepare and finish a tournament
    for (let i = 1; i <= 4; i++) cy.get('#singleInput').type(`H${i}{enter}`);
    cy.get('#startBtn').click();
    cy.get('#optA').click();
    cy.get('#optA').click();
    // Save result
    cy.get('#shareModalBtn').click();
    // Check history list
    cy.get('#historyList li').should('have.length.at.least', 1);
    // Repeat to exceed 10 entries
    for (let run = 0; run < 10; run++) {
      for (let i = 1; i <= 4; i++) cy.get('#singleInput').type(`X${i}{enter}`);
      cy.get('#startBtn').click(); cy.get('#optA').click(); cy.get('#optA').click();
      cy.get('#shareModalBtn').click();
    }
    cy.get('#historyList li').should('have.length', 10);
  });

  it('Reset clears storage and UI returns to default', () => {
    // Add one item
    cy.get('#singleInput').type('Z1{enter}');
    cy.get('#resetBtn').click();
    // Default state
    cy.get('#listSelector .btn-select.selected').should('have.attr', 'data-list', 'new');
    cy.get('#sizeSelector .btn-select.selected').should('have.attr', 'data-size', '4');
    cy.get('#itemCountInfo').should('contain', '0/4 항목 추가됨 (NEW)');
    // History cleared
    cy.get('#historyList li').should('have.length', 0);
  });
});
