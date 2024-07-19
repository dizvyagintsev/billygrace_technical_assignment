import { test, expect } from '@playwright/test';

const BASE_URL = 'http://localhost:3000';
const CORRECT_EMAIL = 'demo@minimals.cc';
const CORRECT_PASSWORD = 'demo1234';

async function assert_login_form(page) {
  await expect(page.locator('form')).toBeVisible();
  await expect(page.locator('input[name="email"]')).toBeVisible();
  await expect(page.locator('input[name="password"]')).toBeVisible();
  await expect(page.locator('button[type="submit"]')).toBeVisible();
}

async function assert_invalid_creds_alert(page) {
  const alertMessage = page.locator('div.MuiAlert-message').nth(1);
  await expect(alertMessage).toBeVisible();
  await expect(alertMessage).toHaveText('Invalid email or password');
}

test.describe('Login Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(BASE_URL);
  });

  test('1. On first load we see login form', async ({ page }) => {
    await assert_login_form(page);
  });

  test('2. If email is incorrect we stay on login page', async ({ page }) => {
    await page.fill('input[name="email"]', 'wrong@example.com');
    await page.fill('input[name="password"]', 'password123');
    await page.click('button[type="submit"]');

    await assert_invalid_creds_alert(page);
    await assert_login_form(page);
  });

  test('3. If password is incorrect we stay on login page', async ({ page }) => {
    await page.fill('input[name="email"]', CORRECT_EMAIL);
    await page.fill('input[name="password"]', 'wrongpassword');
    await page.click('button[type="submit"]');

    await assert_invalid_creds_alert(page);
    await assert_login_form(page);
  });

  test('4. If email and password correct dashboard opens', async ({ page }) => {
    await page.fill('input[name="email"]', CORRECT_EMAIL);
    await page.fill('input[name="password"]', CORRECT_PASSWORD);
    await page.click('button[type="submit"]');

    await page.waitForSelector('form', { state: 'detached' });
  });
});

test.describe('Dashboard Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(BASE_URL);
    await page.fill('input[name="email"]', CORRECT_EMAIL);
    await page.fill('input[name="password"]', CORRECT_PASSWORD);
    await page.click('button[type="submit"]');
  });

  test('5. Dashboard has non-empty datagrid', async ({ page }) => {
    await page.waitForSelector('.MuiDataGrid-row', { state: 'visible' });
    const rows_number = await page.locator('.MuiDataGrid-row').count();
    expect(rows_number).toBeGreaterThan(0);

    const columns = await page.locator('.MuiDataGrid-columnHeaderTitleContainer').all();
    const columnNames = await Promise.all(columns.map(async (column) => column.textContent()));
    expect(columnNames).toEqual(['Ad Copy', 'Spend', 'Clicks', 'Impressions', 'Sessions', 'ROAS']);
  });

  test('6. Dashboard has line and buble charts', async ({ page }) => {
    await page.waitForSelector('#chart');
    const chartDiv = page.locator('#chart');
    await expect(await chartDiv.count()).toEqual(2);
    await expect(chartDiv.nth(0)).toBeVisible();
    await expect(chartDiv.nth(1)).toBeVisible();
  });
});
